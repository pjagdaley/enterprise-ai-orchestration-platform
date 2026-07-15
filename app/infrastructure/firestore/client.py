"""
Firestore client configuration.
"""

from firebase_admin import credentials
from firebase_admin import firestore
import firebase_admin

from app.core.config import settings


class FirestoreProvider:
    """
    Singleton wrapper around the Firestore client.
    """

    _db = None

    @classmethod
    def get_client(cls):
        """
        Returns a Firestore client instance.
        """

        if cls._db is not None:
            return cls._db

        #
        # Initialize Firebase only once
        #
        if not firebase_admin._apps:
            credential = credentials.Certificate(
                settings.firebase_credentials_path
            )

            firebase_admin.initialize_app(credential)

        cls._db = firestore.client()

        return cls._db