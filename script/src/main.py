import asyncio

from user_application_update import executable_functions as user_application_update_functions

targets = user_application_update_functions


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    gather = asyncio.gather(*[func() for func in targets])
    loop.run_until_complete(gather)


if __name__ == "__main__":
    main()
