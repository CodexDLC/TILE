class ArticleBook {
    constructor(root) {
        this.root = root;
        this.viewport = root.querySelector("[data-book-viewport]");
        this.flow = root.querySelector("[data-book-flow]");
        this.controls = root.querySelector("[data-book-controls]");
        this.previous = root.querySelector("[data-book-prev]");
        this.next = root.querySelector("[data-book-next]");
        this.status = root.querySelector("[data-book-status]");
        this.related = root.parentElement.querySelector("[data-book-related]");
        this.motion = matchMedia("(prefers-reduced-motion: reduce)");
        this.index = 0;
        this.count = 1;
        this.step = 0;
        this.anchor = null;
        this.wheelTime = -Infinity;
        this.wheelDistance = 0;
        this.wheelTurned = false;
        this.touchStart = null;

        root.classList.add("is-paged");
        this.measure();
        this.openHash();
        new ResizeObserver(() => this.measure()).observe(this.viewport);
        document.fonts?.ready.then(() => this.measure());
        this.flow.addEventListener("load", () => this.measure(), true);
        this.previous.addEventListener("click", () => this.turn(-1));
        this.next.addEventListener("click", () => this.turn(1));
        this.viewport.addEventListener("wheel", event => this.onWheel(event), { passive: false });
        this.viewport.addEventListener("pointerdown", event => {
            this.touchStart = event.pointerType === "touch" ? [event.clientX, event.clientY] : null;
        });
        this.viewport.addEventListener("pointerup", event => {
            if (!this.touchStart) return;
            const [x, y] = this.touchStart;
            this.touchStart = null;
            const distance = event.clientX - x;
            if (Math.abs(distance) > 48 && Math.abs(distance) > Math.abs(event.clientY - y) * 1.35) {
                this.turn(distance < 0 ? 1 : -1);
            }
        });
        this.viewport.addEventListener("pointercancel", () => { this.touchStart = null; });
        root.addEventListener("keydown", event => {
            if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
            const direction = { ArrowLeft: -1, ArrowRight: 1 }[event.key];
            if (direction && this.canTurn(direction)) {
                event.preventDefault();
                this.turn(direction);
            }
        });
        this.flow.addEventListener("focusin", event => this.reveal(event.target));
        window.addEventListener("hashchange", () => this.openHash());
    }

    measure() {
        if (!this.root.classList.contains("is-paged")) return;
        this.finishTurn?.();
        const style = getComputedStyle(this.flow);
        this.columns = Number(style.columnCount);
        this.gap = Number.parseFloat(style.columnGap) || 0;
        this.width = this.viewport.getBoundingClientRect().width;
        if (this.width === 0) return;
        if (this.flow.scrollHeight > this.flow.clientHeight + 2) {
            // An oversized indivisible block needs the continuous article layout.
            this.root.classList.remove("is-paged");
            this.flow.style.transform = "";
            this.controls.hidden = true;
            if (this.related) this.related.hidden = false;
            return;
        }
        this.step = this.width + this.gap;
        this.count = Math.max(1, Math.ceil((this.flow.scrollWidth + this.gap - 2) / this.step));
        const anchorPage = this.anchor ? this.pageOf(this.anchor) : this.index;
        this.show(anchorPage);
    }

    pageOf(element) {
        const origin = this.flow.getBoundingClientRect().left;
        return Math.max(0, Math.floor((element.getClientRects()[0]?.left - origin + 2) / this.step) || 0);
    }

    show(index) {
        this.index = Math.min(this.count - 1, Math.max(0, index));
        this.positionFlow(this.index);
        this.previous.disabled = !this.canTurn(-1);
        this.next.disabled = !this.canTurn(1);
        this.status.value = `${this.index + 1} / ${this.count}`;
        this.controls.hidden = this.count === 1;
        if (this.related) this.related.hidden = this.index < this.count - 1;

        const viewport = this.viewport.getBoundingClientRect();
        this.anchor = [...this.flow.querySelectorAll("h1, h2, h3, p, figure, li, dt")].find(element =>
            [...element.getClientRects()].some(rect => rect.left >= viewport.left - 2 && rect.left < viewport.right)
        ) ?? null;
    }

    positionFlow(index) {
        this.flow.style.transform = `translateX(${-index * this.step}px)`;
    }

    canTurn(direction) {
        const target = this.index + direction;
        return this.root.classList.contains("is-paged") && target >= 0 && target < this.count;
    }

    reveal(element) {
        if (!this.root.classList.contains("is-paged") || !this.step || !this.flow.contains(element)) return;
        const index = this.pageOf(element);
        this.finishTurn?.();
        if (index !== this.index) {
            this.show(index);
        }
    }

    openHash() {
        try {
            const target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
            if (target) this.reveal(target);
        } catch (error) {
            if (!(error instanceof URIError)) throw error;
        }
    }

    onWheel(event) {
        if (event.ctrlKey || event.altKey || event.metaKey || event.shiftKey) return;
        const delta = Math.abs(event.deltaX) > Math.abs(event.deltaY) ? event.deltaX : event.deltaY;
        const direction = Math.sign(delta);
        const now = performance.now();
        if (now - this.wheelTime > 180) {
            this.wheelTurned = false;
            this.wheelDistance = 0;
        }
        this.wheelTime = now;
        if (!direction || !this.canTurn(direction)) return;
        event.preventDefault();
        if (this.wheelTurned || this.finishTurn) return;
        this.wheelDistance += delta * (event.deltaMode === 1 ? 16 : event.deltaMode === 2 ? this.width : 1);
        if (Math.abs(this.wheelDistance) >= 32) {
            this.wheelTurned = true;
            this.turn(direction);
        }
    }

    turn(direction) {
        if (!this.canTurn(direction) || this.finishTurn) return;
        const nextIndex = this.index + direction;
        if (this.motion.matches || !Element.prototype.animate) {
            this.show(nextIndex);
            return;
        }

        const forward = direction > 0;
        const leaf = document.createElement("div");
        leaf.className = `book-turn book-turn-${forward ? "forward" : "back"}`;
        leaf.setAttribute("aria-hidden", "true");
        leaf.inert = true;
        leaf.append(this.leafFace(this.index, forward), this.leafFace(nextIndex, !forward));
        const shadow = document.createElement("div");
        shadow.className = forward ? "book-turn-shadow" : "book-turn-shadow book-turn-shadow-back";
        shadow.setAttribute("aria-hidden", "true");
        const frame = this.viewport.parentElement;
        const restingPage = this.columns === 2 ? this.leafFace(this.index, !forward) : null;
        if (restingPage) {
            restingPage.classList.add("book-turn-resting");
            restingPage.setAttribute("aria-hidden", "true");
            restingPage.inert = true;
            frame.append(restingPage);
        }
        frame.append(shadow, leaf);
        this.positionFlow(nextIndex);
        const duration = 700;
        const animation = leaf.animate(
            [
                { transform: "rotateY(0deg)" },
                { transform: `rotateY(${direction * -180}deg)` },
            ],
            { duration, easing: "cubic-bezier(.36,.12,.38,1)" },
        );
        const shadowAnimation = shadow.animate(
            [
                { opacity: 0, offset: 0, easing: "ease-in-out" },
                { opacity: 1, offset: .35, easing: "ease-in-out" },
                { opacity: 0, offset: .94 },
                { opacity: 0, offset: 1 },
            ],
            { duration },
        );
        this.finishTurn = () => {
            animation.cancel();
            shadowAnimation.cancel();
            leaf.remove();
            shadow.remove();
            restingPage?.remove();
            this.finishTurn = null;
            this.show(nextIndex);
        };
        animation.onfinish = () => {
            if (leaf.isConnected) this.finishTurn();
        };
    }

    leafFace(index, right) {
        const face = document.createElement("div");
        face.className = `book-turn-face book-turn-face-${right ? "right" : "left"}`;
        const snapshot = this.flow.cloneNode(true);
        snapshot.removeAttribute("data-book-flow");
        snapshot.querySelectorAll("[id]").forEach(element => element.removeAttribute("id"));
        snapshot.classList.add("book-turn-snapshot");
        snapshot.style.width = `${this.width}px`;
        snapshot.style.transform = "none";
        const innerPad = this.columns === 2 && right ? `${this.gap / 2}px` : "var(--book-pad-inline)";
        const columnStep = this.columns === 2 && right ? this.step / 2 : 0;
        snapshot.style.left = `calc(${innerPad} - ${index * this.step + columnStep}px)`;
        face.append(snapshot);
        return face;
    }
}

const article = document.querySelector("[data-article-book]");
if (article && CSS.supports("overflow", "clip")) new ArticleBook(article);
