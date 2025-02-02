import { useState } from "react";

function useSubmitButton(){
     const [submitButton, setActive] = useState(false);
    return {submitButton, setActive};
}

export default useSubmitButton;