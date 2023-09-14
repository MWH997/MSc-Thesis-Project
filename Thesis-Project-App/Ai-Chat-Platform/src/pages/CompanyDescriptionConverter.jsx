import { useState } from 'react';
import CompanyDescriptionForm from '../components/CompanyDescriptionForm';
import AimlFormReadOnly from '../components/AimlFormReadOnly';

const CompanyDescriptionConverter = () => {
  const [description, setDescription] = useState('');
  const [aiml, setAiml] = useState('');

  return (
    <div className="containerWrap">
      <div className="hero text-2xl font-bold p-5">Company Description</div>
      <div className="grid flex-grow card bg-base-300 rounded-box place-items-center p-5">
        <CompanyDescriptionForm description={description} setDescription={setDescription} setAiml={setAiml} />
      </div>
      <div className="hero text-2xl font-bold p-5">Converted AIML</div>
      <div className="grid flex-grow card bg-base-300 rounded-box place-items-center p-5">
        <AimlFormReadOnly aiml={aiml} />
      </div>
    </div>
  );
};

export default CompanyDescriptionConverter;
