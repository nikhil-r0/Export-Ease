# ExportEase: Your One-Stop Solution for Exporting Queries

**ExportEase** is an all-in-one platform designed to simplify exporting for small and medium businesses (SMBs). By leveraging cutting-edge AI and real-time data integrations, ExportEase aims to address exporters' challenges, including navigating complex trade regulations, finding incentives, and ensuring compliance.

## 🌟 Features

### Current Features
1. **Realtime Tariff Details**  
   Integrates with the US HTS API to fetch real-time tariff details based on the Harmonized System (HS) code, enabling exporters to get accurate data for their products.

2. **AI-Driven Onboarding Guidance**  
   Utilizes **Google’s Gemini API** to generate detailed onboarding instructions for exporters, pulling insights from a custom dataset built from regulatory and incentive documents.

3. **Guides & Resources Pages**  
   - **Guides:** Step-by-step articles covering compliance, documentation, and exporting best practices.  
   - **Resources:** Links to official standards and incentive programs (e.g., ASTM, RoDTEP, and CPSC).

4. **Interactive Questionnaire**  
   An exporter-centric questionnaire that provides tailored insights based on product details (currently limited due to backend deployment constraints).

---

## 🎯 Vision
ExportEase is designed to solve the fragmented nature of export-related resources by providing a **centralized platform**. With a user-friendly interface and intelligent backend, it reduces the time, effort, and uncertainty exporters face when navigating global trade requirements.

---

## 🚀 Future Roadmap

### To-Do List
1. **Cloud-Based Dataset**  
   Transition from static files to a cloud-based dataset for real-time updates on guides, regulations, and incentives.

2. **AI Chatbot for Export Queries**  
   Build a chatbot that leverages guides and resources to answer user queries, providing exporters with instant assistance.

3. **Backend Deployment**  
   Deploy the backend to make the questionnaire fully functional. The frontend is already deployed.

4. **Incentive Program Integration**  
   Properly integrate RoDTEP and other incentive programs. This requires standardizing HS code mappings, as current inconsistencies across government resources pose challenges.

5. **ML-Based HS Code Finder**  
   Develop an ML-powered tool to identify HS codes based on product descriptions, simplifying the process for exporters.

---

## 💡 Challenges Faced
- **Non-Standard HS Codes:** Inconsistent naming and codes across government documents complicate mapping and integration.  
- **Fragmented Resources:** Compliance and incentive regulations are scattered across various platforms, making consolidation a time-consuming task.  
- **Time Constraints:** While the vision for ExportEase is expansive, time limitations restricted us from fully realizing its potential in this phase.

---

## 📂 Project Structure

### 1. Frontend
Located in the `expo-ease` submodule. The frontend is fully deployed and provides:  
- User-friendly guides and resources.  
- An intuitive questionnaire (awaiting backend deployment).  

**How to Run:**  
Refer to the [frontend README](./expo-ease/README.md) for setup instructions.

### 2. Backend
Located in the `backend` folder. The backend handles:  
- API integration for real-time tariff details.  
- AI-powered onboarding guidance.  

**How to Run:**  
Refer to the [backend README](./backend/README.md) for setup instructions.

---

## 🙏 Acknowledgments
We acknowledge the complexities of exporting, including fragmented compliance data, inconsistent HS code standards, and the lack of a unified platform. ExportEase is our effort to address these challenges with technology, and while there's much work to be done, this is just the beginning of our journey to simplify global trade for Indian SMBs.

---

Thank you for supporting **ExportEase**! Stay tuned for more updates as we continue to build and refine this platform.
