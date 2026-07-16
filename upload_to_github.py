import requests
import base64
import os
import json
import argparse


def list_files_in_repo(owner, repo, token, path=""):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {"Authorization": f"token {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"获取仓库文件列表失败: {e}")
        return []


def upload_file(owner, repo, token, file_path, content):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    headers = {"Authorization": f"token {token}", "Content-Type": "application/json"}
    
    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    
    existing_files = list_files_in_repo(owner, repo, token)
    sha = None
    
    for f in existing_files:
        if f['name'] == os.path.basename(file_path):
            sha = f['sha']
            break
    
    data = {
        "message": f"Add {file_path}",
        "content": encoded_content
    }
    
    if sha:
        data["sha"] = sha
    
    try:
        response = requests.put(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        print(f"✓ 成功上传: {file_path}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"✗ 上传失败 {file_path}: {e}")
        try:
            print(f"  响应: {response.text[:200]}")
        except:
            pass
        return False


def upload_directory(owner, repo, token, local_dir, remote_dir=""):
    success_count = 0
    fail_count = 0
    
    for root, dirs, files in os.walk(local_dir):
        for file in files:
            if file.startswith('.') or file.endswith('.pyc') or '__pycache__' in root:
                continue
            
            local_path = os.path.join(root, file)
            
            rel_path = os.path.relpath(local_path, local_dir)
            if remote_dir:
                remote_path = os.path.join(remote_dir, rel_path)
            else:
                remote_path = rel_path
            
            remote_path = remote_path.replace('\\', '/')
            
            try:
                with open(local_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if upload_file(owner, repo, token, remote_path, content):
                    success_count += 1
                else:
                    fail_count += 1
            except UnicodeDecodeError:
                try:
                    with open(local_path, 'rb') as f:
                        content = f.read().decode('latin-1')
                    
                    if upload_file(owner, repo, token, remote_path, content):
                        success_count += 1
                    else:
                        fail_count += 1
                except Exception as e:
                    print(f"✗ 读取文件失败 {local_path}: {e}")
                    fail_count += 1
            except Exception as e:
                print(f"✗ 读取文件失败 {local_path}: {e}")
                fail_count += 1
    
    return success_count, fail_count


def main():
    parser = argparse.ArgumentParser(description='上传项目到GitHub仓库')
    parser.add_argument('--token', required=True, help='GitHub Personal Access Token')
    parser.add_argument('--username', required=True, help='GitHub用户名')
    parser.add_argument('--repo', required=True, help='GitHub仓库名')
    parser.add_argument('--dir', default=None, help='本地项目目录(默认为脚本所在目录)')
    args = parser.parse_args()
    
    token = args.token
    username = args.username
    repo_name = args.repo
    
    if args.dir:
        project_dir = args.dir
    else:
        project_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("=" * 50)
    print("  GitHub项目上传工具")
    print("=" * 50)
    print(f"\n正在上传项目到 https://github.com/{username}/{repo_name}")
    print(f"项目目录: {project_dir}")
    
    print("\n即将上传的文件:")
    file_list = []
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            if file.startswith('.') or file.endswith('.pyc') or '__pycache__' in root:
                continue
            local_path = os.path.join(root, file)
            rel_path = os.path.relpath(local_path, project_dir)
            file_list.append(rel_path)
            print(f"  {rel_path}")
    
    print(f"\n共 {len(file_list)} 个文件")
    
    print("\n开始上传...")
    success, fail = upload_directory(username, repo_name, token, project_dir)
    
    print("\n" + "=" * 50)
    print(f"上传完成!")
    print(f"成功: {success} 个文件")
    print(f"失败: {fail} 个文件")
    print(f"仓库地址: https://github.com/{username}/{repo_name}")
    print("=" * 50)


if __name__ == "__main__":
    main()