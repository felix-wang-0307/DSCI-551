#!/usr/bin/env python3
"""
Script to rename image files in hw3 for better readability
Based on the content described in hw3.md
"""

import os
import shutil
from pathlib import Path

def rename_images():
    """Rename image files based on their content described in hw3.md"""
    
    # Define the image directory
    image_dir = Path("image/hw3")
    
    # Check if directory exists
    if not image_dir.exists():
        print(f"Error: Directory {image_dir} not found!")
        return
    
    # Define the mapping of old names to new names
    rename_mapping = {
        "1761096290748.png": "ER_diagram.png",
        "1761097122570.png": "question1_task_file_counts.png",
        "1761097215487.png": "question2_tasks_with_multiple_models.png", 
        "1761097238286.png": "question3_tasks_different_users.png",
        "1761097261677.png": "question4_avg_file_size_speech_recognition.png",
        "1761097286379.png": "question5_most_downloaded_files.png",
        "1761097313334.png": "question6_users_download_own_files.png",
        "1761097339841.png": "question7_users_download_both_f1_f2.png",
        "1761097361445.png": "question8_language_generation_max_params.png"
    }
    
    print("Starting image renaming process...")
    print(f"Working directory: {os.getcwd()}")
    print(f"Image directory: {image_dir.absolute()}")
    
    # List all files in the directory
    existing_files = list(image_dir.glob("*.png"))
    print(f"\nFound {len(existing_files)} PNG files:")
    for f in existing_files:
        print(f"  - {f.name}")
    
    # Perform renaming
    renamed_count = 0
    for old_name, new_name in rename_mapping.items():
        old_path = image_dir / old_name
        new_path = image_dir / new_name
        
        if old_path.exists():
            if new_path.exists():
                print(f"Warning: Target file {new_name} already exists, skipping {old_name}")
                continue
                
            try:
                shutil.move(str(old_path), str(new_path))
                print(f"✓ Renamed: {old_name} → {new_name}")
                renamed_count += 1
            except Exception as e:
                print(f"✗ Error renaming {old_name}: {e}")
        else:
            print(f"✗ File not found: {old_name}")
    
    # Check for unrenamed files
    remaining_files = [f for f in image_dir.glob("*.png") 
                      if f.name.startswith("176109") and f.name not in rename_mapping.values()]
    
    if remaining_files:
        print(f"\nUnrenamed files (not referenced in hw3.md):")
        for f in remaining_files:
            print(f"  - {f.name}")
    
    print(f"\nRenaming complete! Successfully renamed {renamed_count} files.")

def update_markdown_references():
    """Update the hw3.md file to use the new image names"""
    
    md_file = Path("hw3.md")
    if not md_file.exists():
        print("hw3.md file not found, skipping markdown update")
        return
    
    # Read the markdown file
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define replacements
    replacements = {
        "![1761096290748](image/hw3/1761096290748.png)": "![ER Diagram](image/hw3/ER_diagram.png)",
        "![1761097122570](image/hw3/1761097122570.png)": "![Question 1 Result](image/hw3/question1_task_file_counts.png)",
        "![1761097215487](image/hw3/1761097215487.png)": "![Question 2 Result](image/hw3/question2_tasks_with_multiple_models.png)",
        "![1761097238286](image/hw3/1761097238286.png)": "![Question 3 Result](image/hw3/question3_tasks_different_users.png)",
        "![1761097261677](image/hw3/1761097261677.png)": "![Question 4 Result](image/hw3/question4_avg_file_size_speech_recognition.png)",
        "![1761097286379](image/hw3/1761097286379.png)": "![Question 5 Result](image/hw3/question5_most_downloaded_files.png)",
        "![1761097313334](image/hw3/1761097313334.png)": "![Question 6 Result](image/hw3/question6_users_download_own_files.png)",
        "![1761097339841](image/hw3/1761097339841.png)": "![Question 7 Result](image/hw3/question7_users_download_both_f1_f2.png)",
        "![1761097361445](image/hw3/1761097361445.png)": "![Question 8 Result](image/hw3/question8_language_generation_max_params.png)"
    }
    
    # Apply replacements
    updated_content = content
    replacements_made = 0
    for old_ref, new_ref in replacements.items():
        if old_ref in updated_content:
            updated_content = updated_content.replace(old_ref, new_ref)
            replacements_made += 1
            print(f"✓ Updated markdown reference: {old_ref.split('(')[0]}...")
    
    # Write back to file
    if replacements_made > 0:
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"✓ Updated {replacements_made} markdown references in hw3.md")
    else:
        print("No markdown references needed updating")

if __name__ == "__main__":
    print("Image Renaming Script for HW3")
    print("=" * 40)
    
    # Change to the hw3 directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Rename images
    rename_images()
    
    print("\n" + "=" * 40)
    
    # Update markdown references
    update_markdown_references()
    
    print("\nAll done! 🎉")