import requests
import json
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)


def get_pinterest_profile(username):
    base_url = f"https://www.pinterest.com/{username}/"

    response_cookies = requests.get(base_url)
    cookies = response_cookies.cookies

    new_cookies = {
        "csrftoken": cookies["csrftoken"],
        "_pinterest_sess": cookies["_pinterest_sess"],
        "_auth": cookies["_auth"],
        "_routing_id": cookies["_routing_id"],
        "sessionFunnelEventLogged": "1",
    }

    headers = {
        "authority": "www.pinterest.com",
        "accept": "application/json, text/javascript, */*, q=0.01",
        "accept-language": "en-US,en;q=0.9",
        "referer": "https://www.pinterest.com/",
        "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        "sec-ch-ua-full-version-list": '"Chromium";v="116.0.5845.189", "Not)A;Brand";v="24.0.0.0", "Google Chrome";v="116.0.5845.189"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": '""',
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua-platform-version": '"15.0.0"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "x-app-version": "a7f49c6",
        "x-pinterest-appstate": "active",
        "x-pinterest-pws-handler": "www/[username].js",
        "x-pinterest-source-url": "/trillionsssssss/",
        "x-requested-with": "XMLHttpRequest",
    }

    params = {
        "source_url": f"/{username}/",
        "data": json.dumps(
            {
                "options": {
                    "field_set_key": "profile_grid_item",
                    "filter_stories": False,
                    "sort": "last_pinned_to",
                    "username": username,
                    "bookmarks": [
                        "LT4yMzExNjE0NjIwNjI3MTUxNjZ8MTB8YWI5MDNkYjRkOGJhMmE4YTZiMjdkMmJiZDljYThmMWY3NzcxOWEzZmEwZDA4OTczMTA4ZThmZTgyZjlkMTgzYXxORVd8"
                    ],
                },
                "context": {},
            }
        ),
        "_": "1694601158901",
    }

    response = requests.get(
        "https://www.pinterest.com/resource/BoardsFeedResource/get/",
        params=params,
        cookies=new_cookies,
        headers=headers,
    )

    return response


def save_profile_data(username, response):
    if response.status_code == 200:
        data = response.json()

        # Define the filename for the JSON file
        filename = f"{username}_profile.json"

        # Write the response data to the JSON file
        with open(filename, "w") as json_file:
            json.dump(data, json_file, indent=4)

        print(f"Profile data saved to {filename}")
    else:
        print(f"Failed to retrieve profile data. Status code: {response.status_code}")


def show_profile_data(username):
    response = get_pinterest_profile(username)
    save_profile_data(username, response)

    if response.status_code == 200:
        response_data = response.json()

        # Extract information for each board
        user_data = response_data.get("resource_response", {}).get("data", [])[0]
        boards_data = response_data.get("resource_response", {}).get("data", [])

        # Extract user information
        owner_info = user_data.get("owner", {})
        user_full_name = user_data.get("owner", {}).get("full_name", "N/A")
        user_name = owner_info.get("username", "N/A")
        user_description = user_data.get("description", "N/A")
        user_followers_count = user_data.get("follower_count", 0)
        user_following_count = user_data.get("following_count", 0)
        user_url = user_data.get("user_url", "N/A")
        user_email = user_data.get("email", "N/A")  # Email may not always be available
        user_profile_pic_url = user_data.get("owner", {}).get("image_medium_url", "N/A")

        # Print or process the extracted user information as needed
        # Style and print the extracted user information
        user_info = (
            f"{Fore.BLUE}User Full Name: {user_full_name}\n"
            f"{Fore.BLUE}User Name: {user_name}\n"
            f"{Fore.BLUE}User Description: {user_description}\n"
            f"{Fore.GREEN}Followers Count: {user_followers_count}\n"
            f"{Fore.GREEN}Following Count: {user_following_count}\n"
            f"{Fore.CYAN}User URL: {user_url}\n"
            f"{Fore.CYAN}User Email: {user_email}\n"
            f"{Fore.MAGENTA}Profile Picture URL: {user_profile_pic_url}\n"
        )

        print(user_info)

        print(Fore.RESET + "----------------- Board Informations -----------------")

        # Extract board information
        for board in boards_data:
            board_name = board.get("name", "N/A")
            owner_info = board.get("owner", {})
            owner_full_name = owner_info.get("full_name", "N/A")
            follower_count = board.get("follower_count", 0)
            created_at = board.get("created_at", "N/A")
            description = board.get("description", "N/A")
            privacy = board.get("privacy", "N/A")
            pin_count = board.get("pin_count", 0)
            board_id = board.get("id", "N/A")

            # Style and print the extracted information for each board
            board_info = (
                f"{Fore.RESET}Board Name: {board_name}\n"
                f"{Fore.BLUE}Owner Full Name: {owner_full_name}\n"
                f"{Fore.RED}Follower Count: {follower_count}\n"
                f"{Fore.RED}Board Creation Date: {created_at}\n"
                f"{Fore.CYAN}Board Description: {description}\n"
                f"{Fore.CYAN}Board Privacy: {privacy}\n"
                f"{Fore.GREEN}Pin Count: {pin_count}\n"
                f"{Fore.MAGENTA}Board ID: {board_id}\n"
                f"{Fore.RESET}{'-' * 50}\n"
            )

            print(board_info)


if __name__ == "__main__":
    username = "feastingathome"
    # response = get_pinterest_profile(username)
    # print(response)
    show_profile_data(username)
