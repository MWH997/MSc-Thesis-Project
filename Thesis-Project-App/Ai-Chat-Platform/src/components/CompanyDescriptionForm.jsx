import axios from "axios";
import ReactQuill from "react-quill";
import "react-quill/dist/quill.snow.css";

const CompanyDescriptionForm = ({ description, setDescription, setAiml }) => {
  const auth_key = "DoubleToasted1449";
  const handleSubmit = async () => {
    let data = JSON.stringify({
      text: description,
      auth_key: auth_key,
    });

    let config = {
      method: "post",
      maxBodyLength: Infinity,
      url: "http://127.0.0.1:5000/api/predict",
      headers: {
        auth_key: auth_key,
        "Content-Type": "application/json",
      },
      data: data,
    };

    try {
      const response = await axios.request(config);
      setAiml(response?.data.response);
      console.log(response?.data.response);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="containerWrap flex items-end">
      <div className="p-5">
      <ReactQuill theme="snow" value={description} onChange={setDescription} />
      </div>
      <button className="btn btn-neutral" onClick={handleSubmit}>
        Submit
      </button>
    </div>
  );
};

export default CompanyDescriptionForm;
