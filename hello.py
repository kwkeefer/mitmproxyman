from src.loaders.profile_loaders import load_profile


def main():
    print("Hello from mitmproxyman!")

    p = load_profile("test_profile.yaml")
    print(p.name)
    print(p.scope)


if __name__ == "__main__":
    main()
