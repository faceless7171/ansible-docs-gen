# Role: nginx

No description



## Variables

| Name    | Required | Vars/Defaults | Type   | Value | Description |
|--------|--------|--------|--------|-----|-----|
| ansible_os_family | Yes | - | - | - |  |
| env | False | vars | dict | {'RUNLEVEL': 1} |  |
| nginx_access_log_name | False | defaults | str | access.log |  |
| nginx_error_log_name | False | defaults | str | error.log |  |
| nginx_http_params | False | defaults | dict | {'sendfile': 'on', 'tcp_nopush': 'on', 'tcp_nodelay': 'on', 'keepalive_timeout': '65'} |  |
| nginx_log_dir | False | defaults | str | /var/log/nginx |  |
| nginx_max_clients | False | defaults | int | 512 |  |
| nginx_separate_logs_per_site | False | defaults | bool | False |  |
| nginx_sites | False | defaults | list | [{'server': {'file_name': 'foo', 'listen': 8080, 'server_name': 'localhost', 'root': '/tmp/site1', 'location1': {'name': '/', 'try_files': '$uri $uri/ /index.html'}, 'location2': {'name': '/images/', 'try_files': '$uri $uri/ /index.html'}}}, {'server': {'file_name': 'bar', 'listen': 9090, 'server_name': 'ansible', 'root': '/tmp/site2', 'location1': {'name': '/', 'try_files': '$uri $uri/ /index.html'}, 'location2': {'name': '/images/', 'try_files': '$uri $uri/ /index.html'}}}] |  |
| redhat_pkg | False | vars | list | ['nginx'] |  |
| test | Yes | - | - | - |  |
| ubuntu_pkg | False | vars | list | ['python-selinux', 'nginx'] | &nbsp;Test&nbsp;description<br/> |

## Tasks
* Install the selinux python module
* Copy the epel packages
* Install the nginx packages
* Install the nginx packages
* Create the directories for site specific configurations
* Copy the nginx configuration file
* Copy the nginx default configuration file
* Copy the nginx default site configuration file
* Create the link for site enabled specific configurations
* Create the configurations for sites
* Create the links to enable site configurations
* start the nginx service
* Name does't specified for task: {'file': "path=/etc/nginx/sites-enabled/{{ item['server']['file_name'] }} state=link src=/etc/nginx/sites-available/{{ item['server']['file_name'] }}", 'with_items': "{{ test == 'dfdf' }}", 'when': "nginx_sites|lower != 'none'", 'notify': ['reload nginx']}