const SubmitButton = ({ disabled = false }) => {
  return (
    <button type="submit" disabled={disabled}>
      Create reservation
    </button>
  );
};

export default SubmitButton;
