# Web application and API audit

Map trust boundaries: browser/client to server, public endpoint to privileged handler, server to database or internal service, and application to third-party provider. Verify authentication and authorization on the server for each state-changing or data-returning path. Check object ownership, role changes, tenant context, mass assignment, and alternate routes to the same operation. Client-side checks are usability controls, not authorization evidence.

Follow untrusted input into SQL, commands, templates, HTML/JavaScript, file paths, and outbound requests. Evaluate defenses at the actual sink (parameterization, contextual encoding, constrained commands and paths), rather than treating generic validation as sufficient. For outbound URLs, inspect redirects, DNS and IP validation at connection time, address ranges, protocols, and egress restrictions. Review CSRF/session behavior where cookies authenticate requests, rate limits on abuse-sensitive actions, secret handling, and security-relevant error/log output.

Evidence should identify a reachable caller, controlling actor, vulnerable sink, and consequence. If reachability or deployment configuration is unknown, label the finding suspected and state the missing evidence. Use a local, inert test fixture when it resolves a material uncertainty within the authorized scope.

Review dependency lockfiles, exposed administrative/debug routes, deployment defaults and relevant CI privileges within scope. Verify version-dependent findings against current vendor advisories; distinguish affected versions from reachable exploitation. Inspect credential handling without printing values. Treat scanner output as leads requiring review; missing tooling or uninspected production configuration is a coverage limitation.

Primary guidance:

- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- [OWASP Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html)
- [OWASP SSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)
