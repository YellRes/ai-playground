import os
from supabase import create_client, Client

# 1. 配置认证信息 (建议放入环境变量)
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY") # 使用 service_role key 可以绕过 RLS 权限

# 2. 初始化客户端
supabase: Client = create_client(url, key)

