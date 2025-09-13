# 🏗️ High-Level Design (HLD) Roadmap & Example

This document provides:
1. A structured **roadmap** for approaching HLD interviews.
2. Key aspects to cover while designing.
3. A worked-out **example (URL Shortener)** using the roadmap.

---

## 🚀 Step-by-Step Roadmap for HLD

### 1. Clarify Requirements
- **Functional requirements** → What should the system do?
- **Non-functional requirements (NFRs)** → Latency, throughput, scalability, availability, consistency.
- **Constraints** → Traffic, storage size, read/write ratio, SLA.

✅ Example (URL Shortener):  
- Functional: shorten URL, redirect.  
- Non-functional: low latency, high availability.  
- Constraints: millions of requests/day.  

---

### 2. Define API Contracts (Interface Design)
- Identify the **core APIs** or user interactions.

Example:
- `POST /shorten?url=<long_url>` → `short_url`
- `GET /<short_url>` → redirect

---

### 3. Estimate Scale (Capacity Estimation)
- **Traffic estimation (QPS)**  
- **Storage needs** (data/year)  
- **Bandwidth** (data in/out)  
- **Growth projections**

✅ Example:  
100M URLs → ~20GB metadata storage (200 bytes/record).  

---

### 4. Define High-Level Architecture
Break system into components:  
- Client → API Gateway → Services → DB/Cache → Storage  

Diagram (logical flow):  
```
Clients → Load Balancer → App Servers → Cache (Redis) → Database (MySQL/NoSQL) → Storage
```

---

### 5. Choose Storage Systems
- SQL vs NoSQL  
- File/Object storage (e.g., S3, HDFS)  
- Caching (Redis, Memcached)  

**Justify choices**:  
- Fast lookups → Redis + persistent DB.  

---

### 6. Scalability & Reliability
- Load balancing (round-robin, consistent hashing)  
- Horizontal scaling (stateless servers)  
- Sharding/partitioning  
- Replication (primary-replica for HA)  
- Caching strategy (write-through, write-back, eviction policies)  

---

### 7. Consistency, Availability, Fault Tolerance
- Apply **CAP theorem trade-offs**:
  - Strong vs eventual consistency
  - Leader-follower replication
  - Network failure handling

✅ Example: Messaging system → prioritize availability (eventual consistency ok).  

---

### 8. Performance Optimization
- **CDN** for static assets  
- **Queues** for async processing  
- **Batching & indexing** for queries  
- **Monitoring & alerting** (Prometheus, CloudWatch)  

---

### 9. Security & Compliance
- Authentication (OAuth, JWT)  
- Authorization (RBAC, ABAC)  
- Encryption (at rest + in transit)  
- Rate limiting, throttling  

---

### 10. Future Considerations
- Extensibility (easily add features)  
- Cost optimization  
- Edge cases (malicious inputs, crashes)  
- Deployment (CI/CD, blue-green, canary releases)  

---

## 🗝️ Key Aspects Interviewers Look For
1. **Structured Thinking** – Stepwise breakdown, not rushed solution.  
2. **Trade-offs** – Explain why you choose X over Y.  
3. **Scalability & Reliability** – Address HA, load, partition tolerance.  
4. **Numbers/Estimates** – Even rough calculations matter.  
5. **Security & Monitoring** – Often missed but critical.  
6. **Communication** – Think aloud, use diagrams, ask clarifying questions.  

---

## ✅ Shortcut Framework (R-A-C-E-S)
- **R** → Requirements (functional + non-functional)  
- **A** → API design  
- **C** → Capacity estimation  
- **E** → End-to-end architecture (storage, cache, LB, queue, CDN, etc.)  
- **S** → Security, scalability, monitoring  

---

# 📌 Example HLD: URL Shortener

### 1. Requirements
- **Functional**:  
  - Shorten a given long URL.  
  - Redirect short URL → original long URL.  
- **Non-functional**:  
  - High availability, low latency (<100ms lookup).  
  - Handle millions of requests/day.  

---

### 2. API Design
- `POST /shorten?url=<long_url>` → returns `short_url`  
- `GET /<short_url>` → redirects to original long URL  

---

### 3. Capacity Estimation
- Assume **100M URLs** stored.  
- Each record ≈ 200 bytes.  
- Total storage ≈ 20 GB (fit in modern DBs but will need partitioning as scale grows).  

---

### 4. High-Level Architecture
```
Clients → Load Balancer → App Servers → Cache (Redis) → Database (NoSQL: DynamoDB/Cassandra) → Storage
```

- **App Servers**: Stateless, scalable horizontally.  
- **Cache (Redis)**: For hot URLs (fast redirect).  
- **DB (NoSQL)**: Stores mapping {short → long}.  
- **Storage (S3/HDFS)**: Backup/archive of URL data.  

---

### 5. Storage Choices
- **Primary DB**: NoSQL (Cassandra/DynamoDB) for high write throughput.  
- **Cache**: Redis for fast lookups.  
- **Backup**: S3 for durability.  

---

### 6. Scalability
- **Load Balancer** distributes traffic.  
- **App Servers** are stateless → scale horizontally.  
- **Sharding** in DB by short URL hash.  
- **Replication** for HA.  

---

### 7. Availability & Consistency
- Prioritize **availability** (users should always be redirected).  
- Eventual consistency acceptable for newly shortened URLs.  

---

### 8. Optimization
- **CDN** for frequently accessed URLs.  
- **Bloom filter** to avoid cache misses hitting DB repeatedly.  
- **Monitoring**: Prometheus + alerts.  

---

### 9. Security
- Validate input URLs.  
- Throttle abusive users.  
- Encrypt stored data.  

---

### 10. Future Enhancements
- Expiry time for short URLs.  
- Analytics (click tracking).  
- Custom short domains.  

---
