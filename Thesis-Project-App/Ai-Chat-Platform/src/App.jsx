import CompanyDescriptionConverter from "./pages/CompanyDescriptionConverter";
import Chatbot from "./pages/Chatbot";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";

function App() {
  return (
    <BrowserRouter>
      <div className="w-full">
      <Navbar />
        <div className="bg-base-100 items-center p-5">
          <Routes>
            <Route path="/" element={<CompanyDescriptionConverter />} />
            <Route path="/chatbot" element={<Chatbot chat_type="Original"/>} />
            <Route path="/university" element={<Chatbot chat_type="University"/>} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
