# About Me

<div class="profile-container">
  <div class="profile-image-wrapper">
    <img src="assets/profile.JPG" alt="Dipayan Chattopadhyay" class="profile-image">
  </div>
  <div class="profile-content">
    <p class="intro-text">
      I'm a Senior Software Engineer at AWS with 9+ years of experience developing complex distributed systems. 
      With a passion for scalable architecture and cloud solutions, I've led multiple high-impact projects 
      that have shaped enterprise-grade applications used by millions of users.
    </p>
    <div class="profile-stats">
      <div class="stat">
        <div class="stat-number">9+</div>
        <div class="stat-label">Years Experience</div>
      </div>
      <div class="stat">
        <div class="stat-number">3</div>
        <div class="stat-label">Major Platforms Built</div>
      </div>
      <div class="stat">
        <div class="stat-number">5</div>
        <div class="stat-label">Open Source Projects</div>
      </div>
      <div class="stat">
        <div class="stat-number">10+</div>
        <div class="stat-label">Team Members Led</div>
      </div>
    </div>
  </div>
</div>

## Professional Summary

<div class="summary-section">
  <div class="summary-card">
    <div class="summary-icon">👨‍💻</div>
    <h3>Technical Leadership</h3>
    <p>I lead engineering teams through the full lifecycle of complex software projects. My approach focuses on setting clear architectural direction, establishing best practices, and removing obstacles to enable my team's success.</p>
  </div>
  
  <div class="summary-card">
    <div class="summary-icon">🏗️</div>
    <h3>System Architecture</h3>
    <p>I design scalable, resilient distributed systems that handle high-throughput workloads while maintaining data integrity. My architectures emphasize maintainability, extensibility, and operational excellence.</p>
  </div>
  
  <div class="summary-card">
    <div class="summary-icon">☁️</div>
    <h3>Cloud Solutions</h3>
    <p>With extensive experience in AWS services, I build cloud-native applications that leverage managed services for optimal performance, cost efficiency, and reliability at scale.</p>
  </div>
  
  <div class="summary-card">
    <div class="summary-icon">📊</div>
    <h3>Data Engineering</h3>
    <p>I create data processing pipelines that transform raw information into actionable insights, using both batch and streaming approaches to handle data at scale.</p>
  </div>
</div>

## Education

<div class="education-section">
  <div class="education-card">
    <div class="education-logo uc-logo"></div>
    <div class="education-details">
      <h3>Master of Science in Computer Science</h3>
      <h4>University of Cincinnati</h4>
      <p>Thesis: Data Mining Techniques for Pattern Recognition in Large Datasets</p>
      <p class="education-date">2011 - 2013</p>
    </div>
  </div>
</div>

<style>
.profile-container {
  display: flex;
  align-items: center;
  margin: 2rem 0;
  gap: 2rem;
  flex-wrap: wrap;
}

.profile-image-wrapper {
  flex: 0 0 250px;
}

.profile-image {
  width: 250px;
  height: 250px;
  object-fit: cover;
  border-radius: 50%;
  border: 5px solid var(--md-primary-fg-color);
}

.profile-content {
  flex: 1;
  min-width: 300px;
}

.intro-text {
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.profile-stats {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  margin-top: 2rem;
  gap: 1rem;
}

.stat {
  text-align: center;
  padding: 1rem;
  background-color: rgba(0, 0, 0, 0.03);
  border-radius: 8px;
  min-width: 120px;
  flex: 1;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: bold;
  color: var(--md-primary-fg-color);
}

.stat-label {
  font-size: 0.9rem;
  color: #555;
}

/* Summary Cards */
.summary-section {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.summary-card {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.summary-card:hover {
  transform: translateY(-5px);
}

.summary-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.summary-card h3 {
  margin-top: 0;
  color: var(--md-primary-fg-color);
}

.summary-card p {
  margin-bottom: 0;
  line-height: 1.5;
}

/* Education styling */
.education-section {
  margin: 2rem 0;
}

.education-card {
  display: flex;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  gap: 1.5rem;
  align-items: center;
}

.education-logo {
  width: 80px;
  height: 80px;
  border-radius: 8px;
  background-color: #f0f0f0;
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
  flex-shrink: 0;
}

.uc-logo {
  background-color: #e00122;
  background-image: url("https://www.uc.edu/about/brand/jcr:content/main/responsivegrid_742151756/responsivegrid_71221/responsivegrid_1080770745/responsivegrid_copy_1494065041/responsivegrid_copy_c_2066749028/image_copy.coreimg.svg/1639516394050/uc-logo.svg");
}

.education-details {
  flex: 1;
}

.education-details h3 {
  margin: 0;
  color: var(--md-primary-fg-color);
}

.education-details h4 {
  margin: 0.5rem 0;
  color: #555;
}

.education-date {
  color: #777;
  font-style: italic;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .profile-container {
    flex-direction: column;
    text-align: center;
  }
  
  .profile-image-wrapper {
    margin: 0 auto 1.5rem;
  }
  
  .education-card {
    flex-direction: column;
    text-align: center;
  }
  
  .education-logo {
    margin-bottom: 1rem;
  }
}
</style>
