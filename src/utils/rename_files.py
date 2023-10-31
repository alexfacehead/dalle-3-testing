import os

def rename_files(directory, new_filenames):
    original_filenames = sorted(os.listdir(directory))

    new_filenames_iter = iter(new_filenames)
    for filename in original_filenames:
        if "DALL" in filename:
            try:
                new_filename = next(new_filenames_iter)
            except StopIteration:
                print("No more new filenames available.")
                break

            old_filepath = os.path.join(directory, filename)
            new_filepath = os.path.join(directory, new_filename)
            os.rename(old_filepath, new_filepath)

            print(f"Renamed {filename} to {new_filename}")
        else:
            print(f"Skipping {filename} as it doesn't contain 'DALLE'.")

if __name__ == "__main__":
    directory = input("Enter the directory containing the files to rename: ")
    if directory == "":
        directory = '/Users/alexf/dev/evals-testing/'
        print(directory + "DIR")
    new_filenames = [
        "v1_golden_retriever_park_base.png",
        "v2_dachshund_park_base.png",
        "v3_husky_park_base.png",
        "v4_pug_park_base.png",
        "v1_golden_retriever_park_improved.png",
        "v2_dachshund_park_improved.png",
        "v3_husky_park_improved.png",
        "v4_pug_park_improved.png",
    ]

    rename_files(directory, new_filenames)