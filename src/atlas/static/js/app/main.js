(() => {
    const root = document.documentElement;
    let alpineRegistered = false;

    function storageAvailable() {
        try {
            const key = "__atlas__";
            window.localStorage.setItem(key, key);
            window.localStorage.removeItem(key);
            return true;
        } catch (error) {
            return false;
        }
    }

    function setHeaderHeight() {
        const header = document.querySelector(".header");
        if (!header) {
            return;
        }

        root.style.setProperty("--header-height", `${header.offsetHeight}px`);
    }

    function initStickyHeader() {
        const header = document.querySelector(".header");
        if (!header) {
            return;
        }

        const syncState = () => {
            header.classList.toggle("is-scrolled", window.scrollY > 8);
        };

        setHeaderHeight();
        syncState();

        window.addEventListener("resize", setHeaderHeight, { passive: true });
        window.addEventListener("scroll", syncState, { passive: true });
    }

    function initReadingProgress() {
        const progress = document.querySelector("[data-reading-progress]");
        if (!progress) {
            return;
        }

        const updateProgress = () => {
            const scrollable = document.documentElement.scrollHeight - window.innerHeight;
            const value = scrollable > 0 ? (window.scrollY / scrollable) * 100 : 0;
            progress.style.width = `${Math.min(100, Math.max(0, value))}%`;
        };

        updateProgress();
        window.addEventListener("scroll", updateProgress, { passive: true });
        window.addEventListener("resize", updateProgress, { passive: true });
    }

    function setPersistedValue(key, value) {
        if (!key || !storageAvailable()) {
            return;
        }

        window.localStorage.setItem(key, value);
    }

    function getPersistedValue(key) {
        if (!key || !storageAvailable()) {
            return null;
        }

        return window.localStorage.getItem(key);
    }

    function activateViewSwitch(buttons, activeButton) {
        buttons.forEach((button) => {
            const isActive = button === activeButton;
            button.classList.toggle("active", isActive);
            button.setAttribute("aria-pressed", String(isActive));
        });
    }

    function initViewSwitchers(scope = document) {
        scope.querySelectorAll("[data-view-switch]").forEach((switcher) => {
            const buttons = [...switcher.querySelectorAll("[data-view-value]")];
            if (!buttons.length || switcher.dataset.atlasBound === "true") {
                return;
            }

            const persisted = getPersistedValue(switcher.dataset.persistKey);
            const initial = buttons.find((button) => button.dataset.viewValue === persisted) || buttons.find((button) => button.classList.contains("active")) || buttons[0];

            activateViewSwitch(buttons, initial);

            buttons.forEach((button) => {
                button.addEventListener("click", () => {
                    activateViewSwitch(buttons, button);
                    setPersistedValue(switcher.dataset.persistKey, button.dataset.viewValue || "");
                    switcher.dispatchEvent(new CustomEvent("atlas:view-switch", { bubbles: true, detail: { value: button.dataset.viewValue } }));
                });
            });

            switcher.dataset.atlasBound = "true";
        });
    }

    function setActiveTab(container, tabId) {
        const buttons = [...container.querySelectorAll("[data-tab-button]")];
        const panels = [...container.querySelectorAll("[data-tab-panel]")];

        buttons.forEach((button) => {
            const isActive = button.dataset.tabButton === tabId;
            button.classList.toggle("active", isActive);
            button.setAttribute("aria-selected", String(isActive));
            button.setAttribute("tabindex", isActive ? "0" : "-1");
        });

        panels.forEach((panel) => {
            const isActive = panel.dataset.tabPanel === tabId;
            panel.classList.toggle("is-active", isActive);
            panel.classList.toggle("active", isActive);
            panel.hidden = !isActive;
        });
    }

    function initTabs(scope = document) {
        scope.querySelectorAll("[data-tabs]").forEach((container) => {
            const buttons = [...container.querySelectorAll("[data-tab-button]")];
            if (!buttons.length || container.dataset.atlasBound === "true") {
                return;
            }

            const persisted = getPersistedValue(container.dataset.persistKey);
            const initialButton = buttons.find((button) => button.dataset.tabButton === persisted) || buttons.find((button) => button.classList.contains("active")) || buttons[0];

            setActiveTab(container, initialButton.dataset.tabButton);

            buttons.forEach((button) => {
                button.addEventListener("click", () => {
                    const tabId = button.dataset.tabButton;
                    setActiveTab(container, tabId);
                    setPersistedValue(container.dataset.persistKey, tabId || "");
                });
            });

            container.dataset.atlasBound = "true";
        });
    }

    function initProgressiveEnhancement() {
        root.classList.add("js");
        document.body.classList.add("has-js");
    }

    function bindMenuStateObserver() {
        const menu = document.getElementById("atlas-mobile-menu");
        if (!menu || menu.dataset.menuObserverBound === "true") {
            return;
        }

        const panel = menu.querySelector("[data-mobile-menu-panel]");
        const closeButton = menu.querySelector("[data-mobile-menu-close]");
        const opener = document.querySelector("[data-mobile-menu-opener]");
        if (!panel || !closeButton || !opener) {
            return;
        }

        let isOpen = false;
        let returnFocus = null;
        let bodyWasLocked = false;
        const backgroundState = new Map();
        const focusableElements = () => [...panel.querySelectorAll(
            "a[href], button, input, select, textarea, [tabindex]"
        )].filter((element) => !element.disabled && element.tabIndex >= 0 &&
            !element.closest("[inert]") && element.getClientRects().length);

        const lockBackground = () => {
            [...document.body.children].forEach((element) => {
                if (element === menu || backgroundState.has(element)) {
                    return;
                }
                backgroundState.set(element, element.inert);
                element.inert = true;
            });
        };

        const syncState = () => {
            const nextOpen = menu.style.display !== "none" && !menu.hasAttribute("hidden") &&
                !menu.hasAttribute("x-cloak");
            if (nextOpen === isOpen) {
                return;
            }
            isOpen = nextOpen;
            if (isOpen) {
                returnFocus = opener;
                bodyWasLocked = document.body.classList.contains("menu-open");
                document.body.classList.add("menu-open");
                (focusableElements()[0] || panel).focus({ preventScroll: true });
                lockBackground();
            } else {
                backgroundState.forEach((wasInert, element) => { element.inert = wasInert; });
                backgroundState.clear();
                document.body.classList.toggle("menu-open", bodyWasLocked);
                if (returnFocus && returnFocus.isConnected) {
                    returnFocus.focus({ preventScroll: true });
                }
                returnFocus = null;
            }
        };

        document.addEventListener("keydown", (event) => {
            if (!isOpen) {
                return;
            }
            if (event.key === "Escape") {
                event.preventDefault();
                closeButton.click();
                return;
            }
            if (event.key !== "Tab") {
                return;
            }
            const elements = focusableElements();
            const first = elements[0] || panel;
            const last = elements[elements.length - 1] || panel;
            if (!elements.length || !panel.contains(document.activeElement) ||
                (event.shiftKey && (document.activeElement === first || document.activeElement === panel)) ||
                (!event.shiftKey && (document.activeElement === last || document.activeElement === panel))) {
                event.preventDefault();
                (event.shiftKey ? last : first).focus({ preventScroll: true });
            }
        }, true);

        document.addEventListener("focusin", (event) => {
            if (isOpen && !panel.contains(event.target)) {
                (focusableElements()[0] || panel).focus({ preventScroll: true });
            }
        });

        // Keep newly inserted UI (for example, consent prompts) outside the modal.
        const backgroundObserver = new MutationObserver(() => {
            if (isOpen) {
                lockBackground();
            }
        });
        backgroundObserver.observe(document.body, { childList: true });

        const observer = new MutationObserver(syncState);

        observer.observe(menu, { attributes: true, attributeFilter: ["style", "hidden", "x-cloak"] });
        menu.dataset.menuObserverBound = "true";
        syncState();
    }

    function initHtmx() {
        if (!window.htmx) {
            return;
        }

        window.htmx.config.defaultFocusScroll = true;
        window.htmx.config.scrollBehavior = "smooth";

        document.body.addEventListener("htmx:beforeRequest", (event) => {
            const element = event.detail.elt;
            if (element instanceof HTMLElement) {
                element.setAttribute("aria-busy", "true");
            }
        });

        document.body.addEventListener("htmx:afterRequest", (event) => {
            const element = event.detail.elt;
            if (element instanceof HTMLElement) {
                element.removeAttribute("aria-busy");
            }
        });

        document.body.addEventListener("htmx:afterSwap", (event) => {
            const target = event.detail.target instanceof HTMLElement ? event.detail.target : document;
            initTabs(target);
            initViewSwitchers(target);
            setHeaderHeight();

            if (window.Alpine && target instanceof HTMLElement) {
                window.Alpine.initTree(target);
            }
        });
    }

    function registerAlpine() {
        if (!window.Alpine || alpineRegistered) {
            return;
        }

        const Alpine = window.Alpine;

        Alpine.store("atlas", {
            activeView: "default",
        });

        Alpine.data("appMode", () => ({}));

        Alpine.data("atlasTabs", (initial = "overview", persistKey = null) => ({
            active: persistKey && Alpine.$persist ? Alpine.$persist(initial).as(persistKey) : initial,
            set(tab) {
                this.active = tab;
            },
            is(tab) {
                return this.active === tab;
            },
        }));

        Alpine.data("atlasView", (initial = "grid", persistKey = null) => ({
            current: persistKey && Alpine.$persist ? Alpine.$persist(initial).as(persistKey) : initial,
            set(view) {
                this.current = view;
                Alpine.store("atlas").activeView = view;
            },
            is(view) {
                return this.current === view;
            },
        }));

        alpineRegistered = true;
    }

    document.addEventListener("alpine:init", registerAlpine);

    document.addEventListener("DOMContentLoaded", () => {
        initProgressiveEnhancement();
        initStickyHeader();
        initReadingProgress();
        initTabs();
        initViewSwitchers();
        bindMenuStateObserver();
        initHtmx();
    });

    if (window.Alpine) {
        registerAlpine();
    }

    if (typeof window.__atlasStartAlpine === "function") {
        window.__atlasStartAlpine();
        delete window.__atlasStartAlpine;
    }
})();
