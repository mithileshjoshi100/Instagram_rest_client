import requests
import json
import pandas
base_url = "https://www.instagram.com/api/v1"

headers = {
  ## replace with auth params csrf
}

def get_profile_info(username):
    url = f"{base_url}/users/web_profile_info/?username={username}"
    payload = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response = json.loads(response.text)
    return response["data"]["user"]


def get_followings(id, total_count):
    following_ids = []
    count = 200
    max_id = 0
    while len(following_ids) < total_count:
        url =f"{base_url}/friendships/{id}/following/?count={count}&max_id={max_id}"
        payload = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        response = json.loads(response.text)
        users = response["users"]
        following_ids += users
        max_id = len(following_ids)
    return following_ids

def get_followers(id, total_count):
    following_ids = []
    count = 200
    max_id = 0
    while len(following_ids) < total_count:
        max_string = ""
        if(max_id):
            max_string = f"&max_id={max_id}"
        url =f"{base_url}/friendships/{id}/followers/?count={count}{max_string}&search_surface=follow_list_page"
        payload = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        response = json.loads(response.text)
        users = response["users"]
        following_ids += users
        max_id = response.get("next_max_id",None)
        if max_id is None: break
        max_id =response["next_max_id"]
    return following_ids


# TODO update username
profile = get_profile_info("instagram_username")

id = profile["id"]
following_count = profile["edge_follow"]["count"]
followers_count = profile["edge_followed_by"]["count"]


followings = get_followings(id, following_count)
followings = pandas.DataFrame(followings)
followers = get_followers(id, followers_count)
followers = pandas.DataFrame(followers)


followers.to_csv("followers.csv")
followings.to_csv("followings.csv")


print("connections who not follow you: ")
for index, row in followings.iterrows():
    if(row["username"] not in followers["username"].values):
        print(f"username : {row['username']}, full_name : {row['full_name']}")

