from flask import Flask, request
import requests

app = Flask(__name__)

# This is page access token that you get from facebook developer console.
PAGE_ACCESS_TOKEN = '<Your Page Access Token>'
# This is API key for facebook messenger.
API = "https://graph.facebook.com/v13.0/me/messages?access_token="+PAGE_ACCESS_TOKEN

# This function use for verify token with facebook webhook. So we can verify our flask app and facebook are connected.


@app.route("/", methods=['GET'])
def fbverify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "<Your verify token>":
            return "Verification token missmatch", 403
        return request.args['hub.challenge'], 200
    return "Hello world", 200

# This function return response to facebook messenger.


@app.route("/", methods=['POST'])
def fbwebhook():
    data = request.get_json()
    print(data)
    try:
        # Read messages from facebook messanger.
        message = data['entry'][0]['messaging'][0]['message']
        sender_id = data['entry'][0]['messaging'][0]['sender']['id']
        # Here we get message text and check specific text so we can send response specificaly.
        if message['text'] == "template":
            request_body = {
                "recipient": {
                    "id": sender_id
                },
                "message": {
                    "attachment": {
                        "type": "template",
                        "payload": {
                                "template_type": "generic",
                                "elements": [
                                    {
                                        "title": "Welcome!",
                                        "image_url": "https://raw.githubusercontent.com/fbsamples/original-coast-clothing/main/public/styles/male-work.jpg",
                                        "subtitle": "We have the right hat for everyone.",
                                        "default_action": {
                                            "type": "web_url",
                                            "url": "https://www.originalcoastclothing.com/",
                                            "webview_height_ratio": "tall",
                                        },
                                        "buttons": [
                                            {
                                                "type": "web_url",
                                                "url": "https://www.originalcoastclothing.com/",
                                                "title": "View Website"
                                            }, {
                                                "type": "postback",
                                                "title": "Start Chatting",
                                                "payload": "DEVELOPER_DEFINED_PAYLOAD"
                                            }
                                        ]
                                    },
                                    {
                                        "title": "Welcome!",
                                        "image_url": "https://raw.githubusercontent.com/fbsamples/original-coast-clothing/main/public/styles/male-work.jpg",
                                        "subtitle": "We have the right hat for everyone.",
                                        "default_action": {
                                            "type": "web_url",
                                            "url": "https://www.originalcoastclothing.com/",
                                            "webview_height_ratio": "tall",
                                        },
                                        "buttons": [
                                            {
                                                "type": "web_url",
                                                "url": "https://www.originalcoastclothing.com/",
                                                "title": "View Website"
                                            }, {
                                                "type": "postback",
                                                "title": "Start Chatting",
                                                "payload": "DEVELOPER_DEFINED_PAYLOAD"
                                            }
                                        ]
                                    }
                                ]
                        }
                    }
                }
            }
            response = requests.post(API, json=request_body).json()
            return response
        # here we send button response.
        elif message['text'] == "button":
            request_body = {
                "recipient": {
                    "id": sender_id
                },
                "message": {
                    "attachment": {
                        "type": "template",
                        "payload": {
                            "template_type": "button",
                            "text": "What do you want to do next?",
                            "buttons": [
                                {
                                    "type": "web_url",
                                    "url": "https://www.messenger.com",
                                    "title": "Visit Messenger"
                                },
                                {
                                    "type": "web_url",
                                    "url": "https://www.youtube.com",
                                    "title": "Visit Youtube"
                                },
                            ]
                        }
                    }
                }
            }
            response = requests.post(API, json=request_body).json()
            return response
        # Here we send quick reply response.
        elif message['text'] == "quickr":
            request_body = {
                "recipient": {
                    "id": sender_id
                },
                "messaging_type": "RESPONSE",
                "message": {
                    "text": "Pick a color:",
                    "quick_replies": [
                        {
                            "content_type": "text",
                            "title": "Red",
                            "payload": "<POSTBACK_PAYLOAD>",
                            "image_url": "http://example.com/img/red.png"
                        }, {
                            "content_type": "text",
                            "title": "Green",
                            "payload": "<POSTBACK_PAYLOAD>",
                            "image_url": "http://example.com/img/green.png"
                        }
                    ]
                }
            }
            response = requests.post(API, json=request_body).json()
            return response
        # Here we send simple text response.
        elif message['text'] == "list":
            request_body = {
                "recipient": {
                    "id": "RECIPIENT_ID"
                },
                "message": {
                    "attachment": {
                        "type": "template",
                        "payload": {
                            "template_type": "list",
                            "top_element_style": "compact",
                            "elements": [
                                {
                                    "title": "Classic T-Shirt Collection",
                                    "subtitle": "See all our colors",
                                    "image_url": "https://originalcoastclothing.com/img/collection.png",
                                    "buttons": [
                                        {
                                            "title": "View",
                                            "type": "web_url",
                                            "url": "https://originalcoastclothing.com/collection",
                                            "messenger_extensions": True,
                                            "webview_height_ratio": "tall",
                                            "fallback_url": "https://originalcoastclothing.com/"
                                        }
                                    ]
                                },
                                {
                                    "title": "Classic White T-Shirt",
                                    "subtitle": "See all our colors",
                                    "default_action": {
                                        "type": "web_url",
                                        "url": "https://originalcoastclothing.com/view?item=100",
                                        "messenger_extensions": False,
                                        "webview_height_ratio": "tall"
                                    }
                                },
                                {
                                    "title": "Classic Blue T-Shirt",
                                    "image_url": "https://originalcoastclothing.com/img/blue-t-shirt.png",
                                    "subtitle": "100% Cotton, 200% Comfortable",
                                    "default_action": {
                                        "type": "web_url",
                                        "url": "https://originalcoastclothing.com/view?item=101",
                                        "messenger_extensions": True,
                                        "webview_height_ratio": "tall",
                                        "fallback_url": "https://originalcoastclothing.com/"
                                    },
                                    "buttons": [
                                        {
                                            "title": "Shop Now",
                                            "type": "web_url",
                                            "url": "https://originalcoastclothing.com/shop?item=101",
                                            "messenger_extensions": True,
                                            "webview_height_ratio": "tall",
                                            "fallback_url": "https://originalcoastclothing.com/"
                                        }
                                    ]
                                }
                            ],
                            "buttons": [
                                {
                                    "title": "View More",
                                    "type": "postback",
                                    "payload": "payload"
                                }
                            ]
                        }
                    }
                }

            }
            response = requests.post(API, json=request_body).json()
            return response
        elif message['text'] == "hi":
            request_body = {
                "recipient": {
                    "id": sender_id
                },
                "message": {
                    "text": "hello, world!"
                }
            }
            response = requests.post(API, json=request_body).json()
            return response
        # Here we send image response.
        elif message['text'] == "image":
            request_body = {
                "recipient": {
                    "id": sender_id
                },
                "message": {
                    "attachment": {
                        "type": "image",
                        "payload": {
                            "url": "http://www.messenger-rocks.com/image.jpg",
                            "is_reusable": True
                        }
                    }
                }
            }
            response = requests.post(API, json=request_body).json()
            return response
        # Here we send receipt type response.
        elif message['text'] == "receipt":
            request_body = {
                "recipient": {
                    "id": "<PSID>"
                },
                "message": {
                    "attachment": {
                        "type": "template",
                        "payload": {
                            "template_type": "receipt",
                            "recipient_name": "Stephane Crozatier",
                            "order_number": "12345678902",
                            "currency": "USD",
                            "payment_method": "Visa 2345",
                            "order_url": "http://originalcoastclothing.com/order?order_id=123456",
                            "timestamp": "1428444852",
                            "address": {
                                "street_1": "1 Hacker Way",
                                "street_2": "",
                                "city": "Menlo Park",
                                "postal_code": "94025",
                                "state": "CA",
                                "country": "US"
                            },
                            "summary": {
                                "subtotal": 75.00,
                                "shipping_cost": 4.95,
                                "total_tax": 6.19,
                                "total_cost": 56.14
                            },
                            "adjustments": [
                                {
                                    "name": "New Customer Discount",
                                    "amount": 20
                                },
                                {
                                    "name": "$10 Off Coupon",
                                    "amount": 10
                                }
                            ],
                            "elements": [
                                {
                                    "title": "Classic White T-Shirt",
                                    "subtitle": "100% Soft and Luxurious Cotton",
                                    "quantity": 2,
                                    "price": 50,
                                    "currency": "USD",
                                    "image_url": "http://originalcoastclothing.com/img/whiteshirt.png"
                                },
                                {
                                    "title": "Classic Gray T-Shirt",
                                    "subtitle": "100% Soft and Luxurious Cotton",
                                    "quantity": 1,
                                    "price": 25,
                                    "currency": "USD",
                                    "image_url": "http://originalcoastclothing.com/img/grayshirt.png"
                                }
                            ]
                        }
                    }
                }
            }
            response = requests.post(API, json=request_body).json()
            return response

    except:
        # Here we are store the file to our server who send by user from facebook messanger.
        try:
            mess = data['entry'][0]['messaging'][0]['message']['attachments'][0]['payload']['url']
            print("for url-->", mess)
            json_path = requests.get(mess)
            filename = mess.split('?')[0].split('/')[-1]
            open(filename, 'wb').write(json_path.content)
        except:
            print("Noot Found-->")

    return 'ok'


if __name__ == "__main__":
    app.run()
