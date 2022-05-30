=====================================================================================
OIS 2022 - SDK forum -  Solve Ops challenges in a Dev way for Starters with OpenStack
=====================================================================================

.. revealjs-slide::
   :theme: blood

Provisioning - Openstack SDK, Ansible, Terraform
================================================

Page one
--------

Page two
--------

Metrics collection
==================

Statistics reporting
--------------------

openstacksdk can report statistics on individual API requests/responses in several different formats:

* statsd
* influxDB
* prometheus 

clouds.yaml
-----------

.. code-block:: yaml

  metrics:
  statsd:
    host: 127.0.0.1
    port: 8125
    prefix: openstack.api
  clouds:
    mycloud:
      auth:
        auth_url: https://mycloud.example.com:/v3
        project_name: myproject
        username: admin
       domain_name: mytenant
       region_name: europe
  

Sample metrics - statsd
-----------------------

.. code-block:: bash

  Flushing stats at  Fri May 27 2022 13:45:17 GMT+0000 (Coordinated Universal Time)
  { counters:
     { 'statsd.bad_lines_seen': 0,
       'statsd.packets_received': 1,
       'statsd.metrics_received': 2,
       'openstack.api.identity.GET.projects': 1 },
    timers: { 'openstack.api.identity.GET.projects': [ 16.479 ] },
    gauges: { 'statsd.timestamp_lag': 0 },
    timer_data:
     { 'openstack.api.identity.GET.projects':
        { count_90: 1,
          mean_90: 16.479,
          upper_90: 16.479,
          sum_90: 16.479,
          sum_squares_90: 271.557441,
          std: 0,
          upper: 16.479,
          lower: 16.479,
          count: 1,
          count_ps: 0.1,
          sum: 16.479,
          sum_squares: 271.557441,
          mean: 16.479,
          median: 16.479 } },
    counter_rates:
     { 'statsd.bad_lines_seen': 0,
       'statsd.packets_received': 0.1,
       'statsd.metrics_received': 0.2,
       'openstack.api.identity.GET.projects': 0.1 },
    sets: {},
    pctThreshold: [ 90 ] }


Logging from Ansible playbooks
==============================


Module specific log settings
----------------------------

.. code-block:: yaml

   - hosts: localhost
     module_defaults:
       openstack.cloud.image_info:
         sdk_log_path: /home/linux/data/ansible-logging/os-sdk.log
         sdk_log_level: DEBUG
     tasks:
       - name: List images
         openstack.cloud.image_info:

Decommission (cleanup of resources)
===================================

Project cleanup SDK
-------------------

.. code-block:: python

  import openstack
  import queue
  import time

  openstack.enable_logging(debug=True)

  conn = openstack.connect()

  status_queue = queue.Queue()
  conn.project_cleanup(dry_run=True, status_queue=status_queue,
                       filters={'created_at': '2020-07-29T19:00:00Z'}
                      )
  time.sleep(5)
  whilenot status_queue.empty():
      resource = status_queue.get_nowait()
      print('Deleting %s %s %s' % (type(resource),resource.name, resource.id))
  inp = input('Are you sure?')
  ifinp == 'yes':
      conn.project_cleanup(dry_run=False, status_queue=status_queue,
                           filters={'created_at': '2020-07-29T19:00:00Z'}

Project cleanup OSC
-------------------


.. code-block:: bash

  $ openstack project  cleanup --dry-run --created-before 2022-04-18R0024:00:00 --auth-project

Batch processing (scripts)
==========================

Do you need to create a batch of users from a CSV file?
-------------------------------------------------------

Users CSV
---------

.. code-block:: bash

  $ cat users.txt
  username,full name,initial password,email address,user group
  jdily,John Dily,PleaseChangeMe123,John.Dily@example.com,power_user
  sring,Sam Ring,PleaseChangeMe123,Sam.Ring@example.com,admin
  fcruger,Freddy Cruger,PleaseChangeMe123,Freddy.Cruger@example.com,read_only
  ntekon,Nils Tekon,PleaseChangeMe123,Nils.Tekon@example.com,power_user
  jdaniels,Josh Daniels,PleaseChangeMe123,Josh.Daniels@example.com,admin
  sconnors,Sinead Connors,PleaseChangeMe123,Sinead.Connors@example.com,read_only
  jrambo,John Rambo,PleaseChangeMe123,John.Rambo@example.com,power_user
  epresley,Elvis Presley,PleaseChangeMe123,Elvis.Presley@example.com,admin
  kjung,Karl Jung,PleaseChangeMe123,Karl.Jung@example.com,read_only
  dhors,Dennis Hors,PleaseChangeMe123,Dennis.Hors@example.com,power_user


Users python SDK
----------------

.. code-block:: python

  $ cat users.py
  import openstack
  import csv
 
  conn = openstack.connect('domain-scoped')

  with open('users.txt') as csv_file:
      csv_reader = csv.reader(csv_file, delimiter=',')
      line_count = 0
      for row in csv_reader:
          if line_count == 0:
              line_count += 1
              pass
          else:
              conn.identity.create_user(name=row[0], decription=row[1],
                                        password=row[2], email=row[3])
              conn.add_user_to_group(row[0], row[4])
              line_count += 1
      print(f'Processed {line_count-1} lines.')


Would you like to assess the amount of disk space used up by each of your projects?
-----------------------------------------------------------------------------------

.. code-block:: python

  import openstack
  conn = openstack.connect('demo')
  projects=conn.identity.projects()
  for project in projects:
    quota=conn.block_storage.get_quota_set(project, usage=True)
    used_storage=str(quota.usage['gigabytes'])
    total_storage=str(quota.gigabytes)
    print('; '.join(['Project Name: ' + project.name, 'Used Quota: ' + used_storage, 'Total Quota: ' + total_storage]))


Would you like to assess the amount of disk space used up by each of your projects in all domains?
--------------------------------------------------------------------------------------------------

.. code-block:: python

  import openstack
  conn = openstack.connect('demo')
  domains=conn.identity.domains()
  for domain in domains:
      projects=conn.identity.projects(domain_id=domain.id)
      for project in projects:
          quota=conn.block_storage.get_quota_set(project, usage=True)
          used_storage=str(quota.usage['gigabytes'])
          total_storage=str(quota.gigabytes)
          print('; '.join(['Domain Name: ' + domain.name, 'Project Name: ' + project.name, 
    'Used Quota: ' + used_storage, 'Total Quota: ' + total_storage]))


Are all floating IPs are covered by security groups?
----------------------------------------------------

.. code-block:: python

  import openstack
  conn = openstack.connect('adminx')

  import openstack
  conn = openstack.connect('adminx')
  fip={}
  for floating_ip in conn.network.ips():
    if floating_ip.name.startswith('80.158') and floating_ip.port_id:
      port=conn.network.get_port(floating_ip.port_id)
      security_groups=port.security_group_ids
      print(floating_ip.name,security_groups,port.device_owner)