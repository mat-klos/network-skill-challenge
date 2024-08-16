How to setup environment and run tests:

1. Install Docker

2. Create Docker network:

       docker network create--subnet=192.168.100.0/24 custom_network

3. Mock 2 network devices. You can modify MAC OUIs to get a specific vendor name. In this case it is Cisco and Apple device mocked:
 
       docker run--net custom_network--ip 192.168.100.10--mac-address 00:1A:A1:4B:7C:2D-d--name cisco_device alpine sleep infinity
       docker run--net custom_network--ip 192.168.100.11--mac-address AC:87:A3:12:34:56-d--name apple_device alpine sleep infinity

4. Run PostgreSQL Docker container:
   - Go to /PostgreSQL container/
   - Run Docker Compose with:

            docker-compose up

     NOTE: After you do "docker-compose up", if you need any changes in init.sql configuration (e.g. more or less devices initially added to "assets" table, you need to do "docker-compose down" and "docker-compose up" again)

5. Run Network Testing Container:
   - Go to /Network Testing Container/
   - Build it with:
   
           docker build -t network_test_env .

  - Run it:

           docker run --net custom_network -it --name network_test_container network_test_env

6. In Network Testing Container interactive mode (Ubuntu), start tests with:

        pytest VerifyStoredAssetData.py--json-report--json-report-file=report.json-v
    
   NOTE: Test results are visible in Network Testing Container interactive mode (Ubuntu). Test results are stored there in JSON
