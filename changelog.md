## v2.0.0

### Added
- Batch polling loop (`polling_interval`) using `GetUsersRequest` to check all tracked users in one request and catch missed status changes (`[DETAINED]`).
- Support for numeric user IDs in `target_usernames` in addition to `@usernames`.
- Detection for deleted accounts (`Deleted` / `DELETED`) and separate handling for `NoneType` (`Blocked`) vs `UserStatusRecently`.
- Status state normalization (`simplify_status`) to prevent duplicate log entries when the state hasn't changed.
- Auto-reconnect loop (`run_client_forever`) that cleanly restarts the client and polling task after `reconnect_delay` seconds on disconnect or crash.
- Telethon log handler (`TelethonLogHandler`) to forward library warnings and connection errors into `log.txt`.

### Changed
- Added in-memory caching (`get_cached_entity`) for user and chat entities to avoid repeated API requests on every event.
- Updated `UpdateUserStatus` to read `event.status` directly instead of making an extra `get_entity()` call.
- Standardized log formatting with `write_log()` and `write_separator()` and added an `if __name__ == "__main__":` entry point.

### Fixed
- Fixed crashes when logging deleted accounts or users with empty names (`get_safe_name`).
- Fixed startup crashes if a username or ID from `target_usernames` is not found (`ValueError` is now caught and logged).
- Added fallback user ID lookup (`event.from_id.user_id`) in `UpdateChatUserTyping` when `event.user_id` is missing.
- Wrapped event handlers and the polling loop in `try/except` blocks with traceback logging so isolated errors don't crash the script.

```
