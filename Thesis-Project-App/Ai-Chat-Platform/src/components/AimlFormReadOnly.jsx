import XMLViewer from 'react-xml-viewer'
import { useNavigate } from 'react-router-dom';
import axios from 'axios';


const AimlFormReadOnly = ({ aiml }) => {
  const navigate = useNavigate();

  const handleTestClick = async () => {
    //navigate('/chatbot', { aiml });
    const formData = new FormData();
    const blob = new Blob([aiml], { type: "text/xml" });
    console.log(aiml)
    formData.append("file", blob, "aiml.xml");

    try {
    console.log(aiml)
      const response = await axios.post(
        "http://127.0.0.1:5001/upload_aiml",
        formData
      );
      console.log(response.data);
      navigate('chatbot',{aiml});
    } catch (error) {
      console.error("Error uploading AIML:", error);
    }
  }

  return (
    <div className="containerWrap flex items-end">
      <div className="p-10">
        <XMLViewer xml={aiml} />
      </div>
      <button className="btn btn-neutral" onClick={handleTestClick}>Test</button>
    </div>
  );
};

export default AimlFormReadOnly;
