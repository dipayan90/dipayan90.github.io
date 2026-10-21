# Open Source Projects

<div class="projects-intro">
  <p>I'm passionate about open source software and regularly contribute to projects that solve real-world problems. Here are some of the projects I've created or significantly contributed to.</p>
</div>

<div class="projects-grid">

  <div class="project-card">
    <div class="project-header">
      <h3>Spring Actuator CloudWatch</h3>
      <div class="project-links">
        <a href="https://github.com/dipayan90/spring-actuator-cloudwatch" class="project-link" target="_blank">
          <span class="link-icon">📁</span> Repository
        </a>
      </div>
    </div>
    <div class="project-content">
      <p class="project-description">
        A Spring Boot library that enables application metrics to be published directly to AWS CloudWatch, allowing for seamless monitoring of Spring applications in AWS environments.
      </p>
      <div class="project-tech">
        <span class="tech-tag">Java</span>
        <span class="tech-tag">Spring Boot</span>
        <span class="tech-tag">AWS</span>
        <span class="tech-tag">CloudWatch</span>
      </div>
    </div>
  </div>

  <div class="project-card">
    <div class="project-header">
      <h3>Big-data Profiler</h3>
      <div class="project-links">
        <a href="https://github.com/dipayan90" class="project-link" target="_blank">
          <span class="link-icon">👤</span> Nordstrom (org repo)
        </a>
      </div>
    </div>
    <div class="project-content">
      <p class="project-description">
        A library for profiling large datasets in big data environments. It generates statistical metadata about datasets, making it easier to understand data distributions and quality. Contributed to this project while at Nordstrom.
      </p>
      <div class="project-tech">
        <span class="tech-tag">Scala</span>
        <span class="tech-tag">Apache Spark</span>
        <span class="tech-tag">Big Data</span>
        <span class="tech-tag">Data Analysis</span>
      </div>
    </div>
  </div>

  <div class="project-card">
    <div class="project-header">
      <h3>Deep Learning Image Similarity</h3>
      <div class="project-links">
        <a href="https://github.com/dipayan90/deep-learning-image-similarity" class="project-link" target="_blank">
          <span class="link-icon">📁</span> Repository
        </a>
      </div>
    </div>
    <div class="project-content">
      <p class="project-description">
        A tool that uses deep learning techniques to find similar images based on visual content rather than metadata. Useful for recommendation systems and content organization.
      </p>
      <div class="project-tech">
        <span class="tech-tag">Python</span>
        <span class="tech-tag">TensorFlow</span>
        <span class="tech-tag">Deep Learning</span>
        <span class="tech-tag">Computer Vision</span>
      </div>
    </div>
  </div>

  <div class="project-card">
    <div class="project-header">
      <h3>Autoerroretry</h3>
      <div class="project-links">
        <a href="https://github.com/dipayan90/autoerroretry" class="project-link" target="_blank">
          <span class="link-icon">📁</span> Repository
        </a>
      </div>
    </div>
    <div class="project-content">
      <p class="project-description">
        A Java library that provides automatic retry functionality for failed operations, with configurable backoff strategies and failure handling.
      </p>
      <div class="project-tech">
        <span class="tech-tag">Java</span>
        <span class="tech-tag">Resilience</span>
        <span class="tech-tag">Error Handling</span>
        <span class="tech-tag">Distributed Systems</span>
      </div>
    </div>
  </div>

  <div class="project-card">
    <div class="project-header">
      <h3>Time-Series Anomaly Detection</h3>
      <div class="project-links">
        <a href="https://github.com/dipayan90/anomaly-detect-core" class="project-link" target="_blank">
          <span class="link-icon">📁</span> Repository
        </a>
      </div>
    </div>
    <div class="project-content">
      <p class="project-description">
        A library for detecting anomalies in time-series data using statistical methods and machine learning. Useful for monitoring systems and identifying unusual patterns.
      </p>
      <div class="project-tech">
        <span class="tech-tag">Python</span>
        <span class="tech-tag">Machine Learning</span>
        <span class="tech-tag">Time Series</span>
        <span class="tech-tag">Analytics</span>
      </div>
    </div>
  </div>

</div>

## Conference Talk

<div class="talk-card">
  <div class="talk-thumbnail">
    <a href="https://www.youtube.com/watch?v=F8C58OZW3-M" target="_blank">
      <img src="https://img.youtube.com/vi/F8C58OZW3-M/0.jpg" alt="ML Platform Talk">
    </a>
  </div>
  <div class="talk-content">
    <h3>Building an ML Platform at Scale</h3>
    <p>In this talk, I discuss the challenges and solutions in building a scalable ML platform that supports data scientists through the entire model development lifecycle.</p>
    <a href="https://www.youtube.com/watch?v=F8C58OZW3-M" class="md-button md-button--primary" target="_blank">Watch Video</a>
  </div>
</div>

<style>
.projects-intro {
  margin-bottom: 2rem;
  font-size: 1.1rem;
  line-height: 1.6;
  max-width: 800px;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}

.project-card {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  background-color: white;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.project-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
}

.project-header {
  padding: 1.2rem;
  background-color: rgba(0, 0, 0, 0.02);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.project-header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: var(--md-primary-fg-color);
}

.project-links {
  display: flex;
  gap: 0.5rem;
}

.project-link {
  text-decoration: none;
  font-size: 0.8rem;
  font-weight: 500;
  color: #555;
  display: flex;
  align-items: center;
  gap: 0.3rem;
  transition: color 0.2s ease;
}

.project-link:hover {
  color: var(--md-primary-fg-color);
}

.link-icon {
  font-size: 1rem;
}

.project-content {
  padding: 1.2rem;
  flex-grow: 1;
}

.project-description {
  margin: 0 0 1rem 0;
  font-size: 0.95rem;
  color: #555;
  line-height: 1.5;
}

.project-tech {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tech-tag {
  font-size: 0.8rem;
  background-color: rgba(0, 0, 0, 0.05);
  color: #555;
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
  font-weight: 500;
}

.project-footer {
  padding: 1rem 1.2rem;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.github-stats {
  display: flex;
  justify-content: space-around;
}

.github-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.2rem;
}

.stat-icon {
  font-size: 1.2rem;
}

.stat-value {
  font-size: 0.8rem;
  font-weight: 500;
  color: #777;
}

/* Talk styling */
.talk-card {
  display: flex;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-top: 2rem;
}

.talk-thumbnail {
  flex: 0 0 300px;
  overflow: hidden;
}

.talk-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.talk-thumbnail img:hover {
  transform: scale(1.05);
}

.talk-content {
  flex: 1;
  padding: 1.5rem;
}

.talk-content h3 {
  margin-top: 0;
  color: var(--md-primary-fg-color);
}

.talk-content p {
  margin-bottom: 1.5rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .talk-card {
    flex-direction: column;
  }
  
  .talk-thumbnail {
    flex: 0 0 auto;
    height: 200px;
  }
}
</style>

---

*Last reviewed: 2026-10*
