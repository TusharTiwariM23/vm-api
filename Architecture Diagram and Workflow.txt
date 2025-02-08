                   +------------------+
                   |    Internet       |
                   +------------------+
                           |
                           v
               +----------------------+
               |   Load Balancer VM    |  (Nginx, Exposed to Internet)
               +----------------------+
                           |
        -------------------------------------
        |                                   |
        v                                   v
+--------------------+              +--------------------+
|  Application VM 1  |              |  Application VM 2  |
|  (FastAPI Server)  |  <----->     |  (FastAPI Server)  |
+--------------------+              +--------------------+
        |                                   |
        |                                   |
        v                                   v
 +--------------------+
 |   Database VM      |  (PostgreSQL, Secured)
 +--------------------+





Workflow Explanation:

1. **User Request Initiation**  
   - A user sends a request via the internet.
   - The request reaches the Load Balancer VM, which is the only publicly exposed system.

2. **Load Balancer Handling**  
   - The Load Balancer VM (running Nginx) receives the request.
   - It forwards the request to one of the Application VMs using a Round Robin strategy:
     - First request → Application VM 1
     - Second request → Application VM 2
     - Third request → Application VM 1
     - Fourth request → Application VM 2
     - And so on...

3. **Application VM Processing**  
   - The selected Application VM (FastAPI Server) processes the request.
   - If database interaction is needed, it connects to the Database Server (LB VM, which also hosts PostgreSQL).

4. **Database Interaction (if required)**  
   - The Application VM sends queries to the PostgreSQL database.
   - The database processes the queries and returns the result.

5. **Response Transmission**  
   - The Application VM sends the response back to the Load Balancer.
   - The Load Balancer forwards the response to the user over the internet.

### Security Measures:
- **Firewall Rules:** Only necessary ports are open on each VM.
- **Database Access Restriction:** Only Application VMs can communicate with the database.
- **Systemd Services:** All components restart automatically on reboot.
- **Logging & Monitoring:** Nginx logs requests, and Application VMs maintain API logs.

This setup ensures that the system is scalable, secure, and properly load-balanced.
