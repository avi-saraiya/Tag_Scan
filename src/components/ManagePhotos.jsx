import {Button, Fl} from 'antd';

function ManagePhotos(){
    return(
        <div className='buttons-div'>
          <Button id='add-photo'>Attach</Button>
          <Button type = 'primary' id = 'submit-photo'>Submit</Button>
        </div>
    );
}

export default ManagePhotos;