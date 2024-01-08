import os
import shutil


def copy_pdf_files(src_folder, dest_folder):
    for root, _, files in os.walk(src_folder):
        for file in files:
            if file.lower().endswith('.pdf'):
                src_file_path = os.path.join(root, file)
                dest_file_path = os.path.join(dest_folder, file)
                shutil.copy(src_file_path, dest_file_path)


def main():
    # Get the source folder path from the user
    src_folder = input("Please enter the source folder path: ")
    if not os.path.isdir(src_folder):
        print("Invalid source folder path. Script terminated.")
        return

    # Get the destination folder path from the user
    dest_folder = input("Please enter the destination folder path: ")
    if not os.path.isdir(dest_folder):
        print("Invalid destination folder path. Script terminated.")
        return

    # Call the function to copy PDF files
    copy_pdf_files(src_folder, dest_folder)

    print("Copying PDF files completed.")


if __name__ == "__main__":
    main()
