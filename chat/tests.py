from django.test import TestCase

# Create your tests here.
print("{\n  \"message\": \"Привет хочешь машину купить?\"\n}")



{
    "participants": [
        {
            "id": 1,
            "name": "string",
            "phone": "07384848484",
            "avatar": "string",
            "message": [
                {
                    "id": 1,
                    "name": "string",
                    "created_at": "string",
                    "content": "string"
                },
                {
                    "id": 2,
                    "name": "string",
                    "created_at": "string",
                    "content": "string"
                },
                {
                    "id": 3,
                    "name": "string",
                    "created_at": "string",
                    "content": "string"
                }
            ]
        },
        {
            "id": 2,
            "name": "string",
            "phone": "07384848484",
            "avatar": "string",
            "message": [
                {
                    "id": 2,
                    "name": "string",
                    "created_at": "string",
                    "content": "string"
                }
            ]
        }
    ]
}



{
  "participants": [
    0
  ]
}



{
    "unread_messages": [
        {
            "id": 353,
            "chat": 54,
            "sender": 2,
            "sender_name": "me",
            "content": "Еще раз привет",
            "is_read": false,
            "created_at": "25.05.2025 14:35"
        },
        {
            "id": 354,
            "chat": 54,
            "sender": 2,
            "sender_name": "me",
            "content": "мне нужна эта машина",
            "is_read": false,
            "created_at": "25.05.2025 14:35"
        }
    ],
    "read_messages": [
        {
            "id": 352,
            "chat": 54,
            "sender": 2,
            "sender_name": "me",
            "content": "Еще раз привет",
            "is_read": true,
            "created_at": "25.05.2025 14:30"
        },
        {
            "id": 351,
            "chat": 54,
            "sender": 2,
            "sender_name": "me",
            "content": "мне нужна эта машина",
            "is_read": true,
            "created_at": "25.05.2025 14:30"
        }
    ]
}