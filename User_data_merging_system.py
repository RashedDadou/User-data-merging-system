# User_data_merging_system.py

from datetime import datetime, timedelta
import time
import json
from typing import Dict, Any, Optional, List
import numpy as np

class UserDataMergingSystem:
    """
    User Data Merging System (UDMS)
    نظام دمج بيانات المستخدم الذكي - النسخة الكاملة المحسنة
    """

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.created_at = datetime.now()
        self.last_updated = datetime.now()

        # طبقات الذاكرة
        self.short_term_memory: List[Dict] = []
        self.medium_term_memory: Dict = {}
        self.long_term_memory: Dict = {}

        # بيانات المستخدم
        self.profile: Dict[str, Any] = {
            "name": None,
            "preferred_language": "ar",
            "expertise_level": "intermediate",
            "interests": [],
            "avoid_topics": []
        }

        self.preferences: Dict[str, Any] = {
            "response_style": "detailed",
            "humor_level": 0.6,
            "formality": 0.5,
            "max_tokens": 1200
        }

        # حالة النظام
        self.trust_score: float = 0.5
        self.engagement_level: float = 0.0
        self.current_context: Dict = {}

        # الإحصائيات
        self.stats = {
            "total_interactions": 0,
            "total_tokens_used": 0,
            "avg_satisfaction": 0.0,
            "topics_explored": []
        }

        print(f"✅ UserDataMergingSystem تم إنشاؤه للمستخدم: {user_id}")

        # الصندوق الأسود للمواضيع المؤرشفة (المنسية)
        self.black_box_archive: Dict = {}   # topic → {data, archived_at}
        print(f"✅ UserDataMergingSystem تم إنشاؤه مع Forgetting/Remembering Mechanism")

    def _update_engagement_level(self, feedback: Optional[str], message_length: int, tokens_used: Optional[int]):
        if feedback == "positive":
            base = 0.08
        elif feedback == "negative":
            base = -0.04
        else:
            base = 0.025

        length_bonus = min(0.06, message_length / 1500)
        tokens_bonus = min(0.04, (tokens_used or 0) / 800) if tokens_used else 0

        change = base + length_bonus + tokens_bonus
        self.engagement_level = max(0.0, min(1.0, self.engagement_level + change))

    def _update_avg_satisfaction(self, feedback: Optional[str]):
        total = self.stats["total_interactions"]
        new_value = 0.85 if feedback == "positive" else 0.25 if feedback == "negative" else 0.65
        current = self.stats["avg_satisfaction"]
        self.stats["avg_satisfaction"] = (current * (total - 1) + new_value) / total

    def get_merged_context(self, max_short_term: int = 15) -> Dict:
        context = {
            "user_profile": self.profile,
            "preferences": self.preferences,
            "trust_score": round(self.trust_score, 3),
            "engagement_level": round(self.engagement_level, 3),
            "recent_interactions": self.short_term_memory[-max_short_term:],
            "medium_term_summary": self._generate_medium_term_summary(),
            "long_term_summary": self._generate_long_term_summary(),
            "stats": self.stats,
            "current_state": self.current_context
        }

    def _update_trust_score(self, feedback: Optional[str], message_length: int):
        """تحديث ذكي لدرجة الثقة بناءً على جودة التفاعل"""
        if feedback == "positive":
            base = 0.08
            # مكافأة الطول (رسائل مفصلة = أفضل)
            length_bonus = min(0.05, message_length / 2000)
            # مكافأة التكرار (العلاقة تتعزز مع الاستمرار)
            frequency_bonus = min(0.04, self.stats["total_interactions"] / 50)

            total_change = base + length_bonus + frequency_bonus
            self.trust_score = min(1.0, self.trust_score + total_change)

        elif feedback == "negative":
            base = -0.06
            # عقوبة أقل إذا كانت الشكوى قصيرة
            length_penalty = max(-0.03, -message_length / 1500)
            total_change = base + length_penalty
            self.trust_score = max(0.0, self.trust_score + total_change)

        else:
            # neutral أو بدون feedback → تحسن بطيء
            self.trust_score = min(1.0, self.trust_score + 0.012)

    def _extract_topics(self, user_msg: str, grok_resp: str):
        """استخراج مواضيع بسيط + إضافتها إلى الذاكرة المتوسطة"""
        words = user_msg.lower().split()
        potential_topics = [w for w in words if len(w) > 4 and w.isalpha()][:8]

        for topic in potential_topics:
            if topic not in self.stats["topics_explored"]:
                self.stats["topics_explored"].append(topic)

            # إضافة/تحديث في الذاكرة المتوسطة
            if topic not in self.medium_term_memory:
                self.medium_term_memory[topic] = {
                    "count": 0,
                    "first_seen": datetime.now().isoformat()
                }
            self.medium_term_memory[topic]["count"] += 1
            self.medium_term_memory[topic]["last_seen"] = datetime.now().isoformat()

    def _update_medium_and_long_term(self):
        """نقل المواضيع المتكررة إلى الذاكرة طويلة الأمد"""
        for topic, data in list(self.medium_term_memory.items()):
            if data["count"] >= 3:   # حد التكرار
                if topic not in self.long_term_memory:
                    self.long_term_memory[topic] = {
                        "count": data["count"],
                        "interest_level": min(1.0, data["count"] * 0.25),
                        "added_at": datetime.now().isoformat()
                    }
                else:
                    self.long_term_memory[topic]["count"] += data["count"]
                    self.long_term_memory[topic]["interest_level"] = min(1.0,
                        self.long_term_memory[topic]["count"] * 0.25)

    def update_profile(self, new_data: Dict):
        """تحديث ملف المستخدم"""
        self.profile.update(new_data)
        self.last_updated = datetime.now()
        print(f"📝 تم تحديث الملف الشخصي للمستخدم {self.user_id}")

    def serialize(self) -> Dict:
        return {
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
            "profile": self.profile,
            "preferences": self.preferences,
            "trust_score": self.trust_score,
            "engagement_level": self.engagement_level,
            "stats": self.stats,
            "medium_term_count": len(self.medium_term_memory),
            "long_term_count": len(self.long_term_memory),
            "short_term_count": len(self.short_term_memory)
        }

    def _generate_medium_term_summary(self) -> Dict:
        return {
            "active_topics": {k: v["count"] for k, v in self.medium_term_memory.items() if v["count"] >= 2},
            "topic_count": len(self.medium_term_memory)
        }

    def _generate_long_term_summary(self) -> Dict:
        return {
            "main_interests": list(self.long_term_memory.keys())[:10],
            "core_interests": {k: v["interest_level"] for k, v in self.long_term_memory.items()},
            "interaction_count": self.stats["total_interactions"],
            "relationship_age_days": (datetime.now() - self.created_at).days
        }

    def save_to_disk(self, path: str):
        """حفظ حالة الـ UserVertex"""
        data = self.serialize()
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"💾 تم حفظ UserVertex إلى {path}")

    def merge_interaction(self, user_message: str, grok_response: str,
                         feedback: Optional[str] = None,
                         tokens_used: Optional[int] = None,
                         metadata: Dict = None):
        """دمج تفاعل جديد مع كل التحديثات الذكية"""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "grok_response": grok_response,
            "feedback": feedback,
            "tokens_used": tokens_used,
            "metadata": metadata or {}
        }

        # 1. الذاكرة القصيرة
        self.short_term_memory.append(interaction)
        if len(self.short_term_memory) > 25:
            self.short_term_memory.pop(0)

        # 2. الإحصائيات
        self.stats["total_interactions"] += 1
        if tokens_used:
            self.stats["total_tokens_used"] += tokens_used

        self.last_updated = datetime.now()

        # 3. التحديثات الذكية
        self._update_trust_score(feedback, len(user_message))
        self._update_engagement_level(feedback, len(user_message), tokens_used)
        self._update_avg_satisfaction(feedback)

        # 4. استخراج المواضيع وتحديث الذاكرة المتوسطة والطويلة
        self._extract_topics(user_message, grok_response)
        self._update_medium_and_long_term()

        # استخراج المواضيع
        self._extract_topics(user_message, grok_response)

        # آلية النسيان + الاسترجاع (الجديدة)
        self._check_and_unforget(user_message)        # استرجاع إذا ذُكر موضوع قديم
        self._apply_forgetting_mechanism()            # نسيان المواضيع القديمة

        self._update_medium_and_long_term()

        print(f"🔄 تم الدمج | Trust: {self.trust_score:.3f} | Black Box: {len(self.black_box_archive)} موضوع")

        print(f"🔄 تم الدمج | Trust: {self.trust_score:.3f} | Engagement: {self.engagement_level:.2f} | Sat: {self.stats['avg_satisfaction']:.3f}")

    def _apply_forgetting_mechanism(self):
        """نقل المواضيع التي مر عليها 3 أيام أو أكثر إلى الصندوق الأسود"""
        now = datetime.now()
        three_days_ago = now - timedelta(days=3)   # تحتاج import timedelta من datetime

        # فحص الذاكرة المتوسطة
        for topic in list(self.medium_term_memory.keys()):
            last_seen = datetime.fromisoformat(self.medium_term_memory[topic]["last_seen"])
            if last_seen < three_days_ago:
                # نقل إلى الصندوق الأسود
                self.black_box_archive[topic] = {
                    "data": self.medium_term_memory.pop(topic),
                    "archived_at": now.isoformat(),
                    "archive_reason": "temporal_decay"
                }
                print(f"🗄️  تم أرشفة الموضوع '{topic}' في الصندوق الأسود")

        # يمكن تطبيق نفس الشيء على long_term_memory إذا أردت (اختياري)

    def _check_and_unforget(self, user_message: str):
        """استرجاع المواضيع من الصندوق الأسود إذا ذكرها المستخدم"""
        user_lower = user_message.lower()

        for topic in list(self.black_box_archive.keys()):
            if topic.lower() in user_lower or any(word in user_lower for word in topic.lower().split()):
                # استرجاع الموضوع
                archived = self.black_box_archive.pop(topic)
                self.medium_term_memory[topic] = archived["data"]
                self.medium_term_memory[topic]["last_seen"] = datetime.now().isoformat()

                # زيادة الاهتمام لأنه تم تذكره
                if topic in self.long_term_memory:
                    self.long_term_memory[topic]["interest_level"] = min(1.0,
                        self.long_term_memory[topic]["interest_level"] + 0.15)

                print(f"🔄 تم استرجاع الموضوع '{topic}' من الصندوق الأسود (Unforgetting)")
                break   # يكفي استرجاع واحد في كل مرة للكفاءة
