if __name__ == '__main__':
    with open("recipes_links.txt", "r") as f:
        links = f.readlines()
        f.close()
    links.sort()
    with open("recipes_links_sorted.txt", "w") as f:
        for link in links:
            f.write(link)
        f.close()