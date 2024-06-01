class SessionManager:
    _instance = None
    _sessions = {}

    def new(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).new(cls)
        return cls._instance

    def set_session(self, user_id, key, value):
        if user_id not in self._sessions:
            self._sessions[user_id] = {}
        self._sessions[user_id][key] = value

    def get_session(self, user_id, key):
        return self._sessions.get(user_id, {}).get(key)

    def clear_session(self, user_id, key):
        if user_id in self._sessions and key in self._sessions[user_id]:
            del self._sessions[user_id][key]

    def clear_all_sessions(self, user_id):
        if user_id in self._sessions:
            self._sessions[user_id] = {}

session_manager = SessionManager()
