from urllib.parse import urlparse

obs_url = "obs://vendor-sensetime/sensetime/250123/"
parsed_url = urlparse(obs_url)

# 构造基础 OBS 地址
obs_base = f"{parsed_url.scheme}://{parsed_url.netloc}/"
print(obs_base)  # 输出: obs://vendor-sensetime/
