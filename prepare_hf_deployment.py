"""
Helper script to prepare files for Hugging Face deployment
Creates a 'hf_deploy' folder with all necessary files properly named
"""

import os
import shutil

def prepare_deployment():
    print("=" * 60)
    print("  Preparing Hugging Face Deployment Files")
    print("=" * 60)
    print()
    
    # Create deployment folder
    deploy_folder = "hf_deploy"
    if os.path.exists(deploy_folder):
        print(f"📁 Removing existing '{deploy_folder}' folder...")
        shutil.rmtree(deploy_folder)
    
    os.makedirs(deploy_folder)
    print(f"✅ Created '{deploy_folder}' folder")
    print()
    
    # Copy and rename files
    files_to_copy = [
        ("app_hf.py", "app.py"),
        ("requirements_hf.txt", "requirements.txt"),
        ("README_HF.md", "README.md")
    ]
    
    print("📋 Copying files:")
    print("-" * 60)
    
    all_success = True
    for source, dest in files_to_copy:
        try:
            source_path = source
            dest_path = os.path.join(deploy_folder, dest)
            
            if not os.path.exists(source_path):
                print(f"❌ {source} not found!")
                all_success = False
                continue
            
            shutil.copy(source_path, dest_path)
            print(f"✅ {source:25} → {dest}")
            
        except Exception as e:
            print(f"❌ Error copying {source}: {str(e)}")
            all_success = False
    
    print("-" * 60)
    print()
    
    if all_success:
        print("🎉 SUCCESS! Deployment files are ready!")
        print()
        print("📂 Files in 'hf_deploy' folder:")
        print("   ├── app.py")
        print("   ├── requirements.txt")
        print("   └── README.md")
        print()
        print("=" * 60)
        print("  NEXT STEPS:")
        print("=" * 60)
        print()
        print("1. Go to: https://huggingface.co/new-space")
        print("2. Create a new Space:")
        print("   - Name: pdf-rag-system (or your choice)")
        print("   - SDK: Gradio")
        print("   - Visibility: Public")
        print()
        print("3. Upload the 3 files from 'hf_deploy' folder:")
        print("   - Click 'Files' tab")
        print("   - Click 'Add file' → 'Upload files'")
        print("   - Upload all 3 files")
        print("   - Click 'Commit changes'")
        print()
        print("4. Wait 3-5 minutes for build to complete")
        print()
        print("5. Test your deployed app!")
        print()
        print("📖 For detailed instructions, see: DEPLOY_TO_HUGGINGFACE.md")
        print("=" * 60)
        print()
    else:
        print("⚠️  Some files were not copied. Please check the errors above.")
        print()

if __name__ == "__main__":
    prepare_deployment()
