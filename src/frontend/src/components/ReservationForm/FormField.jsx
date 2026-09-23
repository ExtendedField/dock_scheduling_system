const FormField = ({ label, type = "text", min, value, onChange }) => {
  return (
    <label>
      {label}
      <input
        type={type}
        min={min}
        value={value}
        onChange={(event) => onChange(event.target.value)}
        required
      />
    </label>
  );
};

export default FormField;
