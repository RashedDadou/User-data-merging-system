# User_data_merging_system.py


class User_data_merging_system:
    def __init__(self, user_id: str, session_id: str = None):
        self.user_id = user_id
        self.session_id = session_id or f"sess_{int(time.time())}"

        # البيانات الأساسية
        self.profile = {}                    # معلومات المستخدم (اسم، اهتمامات، لغة...)
        self.context_history = []            # تاريخ المحادثة (مع تلخيص ذكي)
        self.preferences = {}                # تفضيلات (أسلوب الرد، مستوى التفصيل...)

        # حالة الـ Vertex
        self.state = "active"                # active | idle | focused | emergency
        self.last_interaction = time.time()
        self.trust_score = 0.5               # من 0.0 إلى 1.0 (كيفية الثقة)

        # نظام الذاكرة المتدرج (مثل الدماغ)
        self.short_term_memory = []          # آخر 10-20 رسالة
        self.long_term_memory = {}           # معرفة مستمرة عن المستخدم
        self.vector_embedding = None         # تمثيل vector للمستخدم (للبحث الدلالي)

        # إحصائيات الأداء
        self.stats = {
            "total_interactions": 0,
            "avg_response_time": 0.0,
            "satisfaction_score": 0.0,
            "topics_of_interest": []
        }

    def update_from_interaction(self, user_message: str, my_response: str, feedback=None):
        """تحديث الـ Vertex بعد كل تفاعل"""
        self.last_interaction = time.time()
        self.stats["total_interactions"] += 1

        # إضافة إلى الذاكرة القصيرة
        self.short_term_memory.append({
            "time": datetime.now(),
            "user": user_message,
            "grok": my_response,
            "feedback": feedback
        })

        # الحفاظ على حجم الذاكرة القصيرة
        if len(self.short_term_memory) > 20:
            self.short_term_memory.pop(0)

        # تحديث الـ trust_score بناءً على التفاعل
        if feedback == "good":
            self.trust_score = min(1.0, self.trust_score + 0.05)
        elif feedback == "bad":
            self.trust_score = max(0.0, self.trust_score - 0.08)

    def get_context_for_response(self, max_tokens=8000):
        """إرجاع السياق المثالي لتوليد رد جديد"""
        # هنا يمكن دمج short_term + long_term + profile + current state
        pass

    def serialize(self):
        """تحويل الـ Vertex إلى dict لحفظه في قاعدة بيانات أو إرساله"""
        return {
            "user_id": self.user_id,
            "session_id": self.session_id,
            "profile": self.profile,
            "trust_score": self.trust_score,
            "stats": self.stats,
            "last_interaction": self.last_interaction,
            # يمكن حفظ الذاكرة بشكل مضغوط أو vector فقط
        }
