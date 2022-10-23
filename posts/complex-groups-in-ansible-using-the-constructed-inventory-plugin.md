# Complex groups in Ansible using the constructed inventory plugin
pubdate: 2022-03-11 17:57 CET

If you ever start working with large, semi-heterogenous groups of VMs and want to manage them with Ansible, you quickly start running into problems trying to make it work with complex groups.

As an example, let's assume we have webservers and jobservers spread out across 2 cloud providers, for 3 different applications, in 3 environments (production, staging, and test). How would you set variables for all webservers for application A? Or all production servers across all providers and applications? Or all webservers, but not jobservers?

The typical solution is to have a lot of duplication in your inventory files. For example:

```yaml
all:
  children:
    env_prod:
      children:
        provider_gcp:
          children:
            type_webserver:
              children:
                app_a:
                  children:
                    app_a_webservers:
                      hosts:
                        web[01:03].app-a.prod.gcp.mycorp.net:
                app_b:
                  children:
                    app_b_webservers:
                      hosts:
                        web[01:03].app-b.prod.gcp.mycorp.net:
            type_jobserver:
              children:
                app_a:
                  children:
                    app_a_jobservers:
                      hosts:
                        job[01:03].app-a.prod.gcp.mycorp.net:
                app_b:
                  children:
                    app_b_jobservers:
                      hosts:
                        job[01:03].app-b.prod.gcp.mycorp.net:
```

Imagine many, many more lines like this, for other environments and providers. The only thing we're **not** repeating in this example is the top-level group (which in this case is `env_prod`, but it's up to you how to structure your hierarchy) and the lowest level group.

## The alternative: Using `constructed`

```yaml
# inventory/main.yml
all:
  children:
    app_a_webservers:
      hosts:
        web[01:03].app-a.prod.gcp.mycorp.net:
        web[01:05].app-a.prod.aws.mycorp.net:
        web[01:02].app-a.stag.gcp.mycorp.net:
        web[01:02].app-a.test.gcp.mycorp.net:
```

The `constructed` plugin lets you define jinja statements for groups. Basically, if the Jinja statement evaluates to `true`, the server will be added to this group. Any built-in Ansible variables (**not** `group_vars`, `host_vars`) are available here, so you can check things like the hostname, which user you're using to connect with, which non-constructed groups the server is a part of, and more. `inventory_hostname` is a useful one, and because it's a string you can do a lot of useful Python operations on it, such as `.split` and `.startswith`. You can also use [Ansible filters](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html).

```yaml
# inventory/zz-constructed.yml
plugin: constructed
strict: true

groups:
  provider_gcp: inventory_hostname.endswith('.gcp.mycorp.net')
  provider_aws: inventory_hostname.split('.')[-3] == 'aws'
  env_prod: inventory_hostname.split('.')[-4] == 'prod'
  env_staging: '.stag.' in inventory_hostname
  env_test: inventory_hostname.endswith(('.stag.gcp.mycorp.net', '.stag.aws.mycorp.net'))
  type_webserver: inventory_hostname.startswith('web')
  type_jobserver: inventory_hostname | regex_search('^job\d+\.')
  app_a: inventory_hostname.split('.')[1] == 'app-a'
  app_b: inventory_hostname | regex_search('[a-z0-9]+\.')
```
