# Offline-first design

The service worker caches the application shell. Approved observations receive client UUIDs and enter local storage; the screen shows network and queue state and allows review. A user-triggered sync sends records sequentially. Successful or duplicate (409) records leave the queue; failures remain. API primary-key uniqueness makes retry idempotent.

Limitations: local storage is neither encrypted nor multi-user, background sync is not used, merge conflicts are not modeled, and cache invalidation is basic. Do not store sensitive information. A pilot needs IndexedDB encryption assessment, authentication, expiry, device management, conflict policy, accessible failure recovery, and sync telemetry.
