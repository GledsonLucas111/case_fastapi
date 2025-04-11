import { CourseService } from "@/services/courseService";
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  TextField,
} from "@mui/material";
import { Fragment, useState } from "react";

export default function FormDialog(props: {id: string}) {
  const [open, setOpen] = useState(false);
  const courseService = new CourseService();

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <Fragment>
      <Button variant="contained" onClick={handleClickOpen} className="h-7">
        Adicionar curso
      </Button>
      <Dialog
        open={open}
        onClose={handleClose}
        slotProps={{
          paper: {
            component: "form",
            onSubmit: (event: React.FormEvent<HTMLFormElement>) => {
              event.preventDefault();
              const formData = new FormData(event.currentTarget);
              const formJson = Object.fromEntries((formData as any).entries());
              const name = formJson.name;
              const video = formJson.video;

              courseService.create({name, video, teacher_id: Number(props.id)}).then((response)=>{
                console.log(response.data)
              }).catch((error)=>{
                console.log(error)
              })
              handleClose();
            },
          },
        }}
      >
        <DialogTitle>Adicionar curso: </DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            required
            margin="dense"
            id="name"
            name="name"
            label="Nome do curso"
            type="text"
            fullWidth
            variant="standard"
          />
          <TextField
            autoFocus
            required
            margin="dense"
            id="video"
            name="video"
            label="Link do video"
            type="text"
            fullWidth
            variant="standard"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancelar</Button>
          <Button type="submit">Cadastrar</Button>
        </DialogActions>
      </Dialog>
    </Fragment>
  );
}
