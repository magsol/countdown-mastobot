import argparse
import simple_image_download.simple_image_download as simp
import os.path

# https://github.com/RiddlerQ/simple_image_download/issues/20

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--keywords", type = str, required = True,
                        help = "Image search terms.")
    parser.add_argument("-n", "--n_images", type = int, default = 25,
                        help = "Number of images to return [DEFAULT: 25].")
    parser.add_argument("-o", "--outfile", type = str, default = "images.txt",
                        help = "Output file for image listings.")
    args = parser.parse_args()

    # Combine the search terms.
    term = (args.keywords).replace(" ", "+")

    # Get the number.
    n = args.n_images

    # Start the download.
    d = simp.Downloader()
    d.download(term, limit = n)

    # Build a text file of image path listings.
    with open(args.outfile, "w") as fp:
        for root, dirs, files in os.walk("simple_images"):
            for f in files:
                fp.write(f"{os.path.join(root, f)}\n")
    
    # All done!
    print("All done downloading images!")
