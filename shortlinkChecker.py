import json
import asyncio
import aiohttp

shortlinks = []

# Load shortlinks from the JSON file
with open("shortlinks.json", "r", encoding="utf8") as shortlink_json:
    if shortlink_json:
        shortlinks = json.load(shortlink_json)


async def checkShortlink(i, session):
    shortlink = shortlinks[i]

    # Make a request to the shortlink, only get the head to make it faster and put less load on the links
    async with session.head("https://dis.gd/" + shortlink["link"], allow_redirects=False) as r:
        # If there is a redirect, get the redirect URL (first redirect)
        if not "location" in r.headers:
            return
        redirect_url = r.headers["location"]

        # If it's different from the current redirect URL
        if (not "redirect" in shortlink) or (shortlink["redirect"] != redirect_url):
            print("Different redirect URL for " + shortlink["link"] + " - New redirect: " + redirect_url)
            shortlinks[i]["redirect"] = redirect_url

        # If there is no type set for the current shortlink, then see if we can set one
        if (not "type" in shortlink) or (not shortlink["type"]):
            print("Missing type for " + shortlink["link"])
            if all(x in redirect_url for x in ["://support.discord", "/articles/"]):
                print(shortlink["link"] + " is an Article")
                shortlinks[i]["type"] = "Article"
            elif ("://medium.com" in redirect_url) or ("://blog.discord" in redirect_url):
                print(shortlink["link"] + " is a Blogpost")
                shortlinks[i]["type"] = "Blogpost"
            elif "://discord.gg/" in redirect_url:
                print(shortlink["link"] + " is a Server Invite")
                shortlinks[i]["type"] = "Server Invite"
            elif all(x in redirect_url for x in ["://discord", "/store"]):
                print(shortlink["link"] + " is a link to a Game Store")
                shortlinks[i]["type"] = "Store"
            elif "://docs.google.com/forms/" in redirect_url:
                print(shortlink["link"] + " is a Form")
                shortlinks[i]["type"] = "Form"


async def main():
    # Start an aiohttp session
    async with aiohttp.ClientSession(loop=asyncio.get_event_loop(), connector=aiohttp.TCPConnector(ssl=False)) as session:
        # Check all the damn links
        await asyncio.gather(*[checkShortlink(shortlink, session) for shortlink in range(len(shortlinks))], return_exceptions=True)

    print("done checking")

    # Write updated stuff to new file
    with open("shortlinkChecker_shortlinks.json", "w", encoding="utf8") as new_shortlink_file:
        new_shortlink_file.write(json.dumps(shortlinks, indent=2))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
