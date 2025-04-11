import { CourseService } from "@/services/courseService";
import { RegistrationService } from "@/services/registrationService";
import { DoneAllOutlined } from "@mui/icons-material";
import {
  Box,
  Button,
  Card,
  CardActions,
  CardContent,
  CardMedia,
  Typography,
} from "@mui/material";
import { Fragment, useEffect, useState } from "react";

type Course = {
  id: string;
  name: string;
  video: string;
  teacher_id: number;
};

type User = {
  email: string;
  id: number;
  name: string;
  role: string;
};
type UserProps = {
  user: User;
};

type Registration = {
  id: number;
  course_id: number;
  student_id: number;
};

export function CardCourse({ user }: UserProps) {
  const courseService = new CourseService();
  const [data, setData] = useState<Course[]>([]);
  const registrationService = new RegistrationService();
  const [verifyCourse, setVerifyCourse] = useState<any>();

  function getUserData() {
    const dados = localStorage.getItem("dataUser");
    if (dados) {
      const user = JSON.parse(dados);
      return user;
    } else {
      console.log("Nenhum usuário encontrado no localStorage.");
    }
  }

  useEffect(() => {
    if (user.role === "teacher") {
      courseService
        .get_course_by_id(user.id.toString())
        .then((response) => {
          setData(response.data);
        })
        .catch((error) => console.log(error));
    }
  }, [user.id]);

  useEffect(() => {
    registrationService
      .list_by_teacher_id(getUserData().id)
      .then((response) => {
        setVerifyCourse(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  }, [data]);
  
  function submit(course_id: number) {
    const userData = getUserData();
    if (!userData) return;
  
    registrationService
      .create({ student_id: userData.id, course_id })
      .then((response) => {
        console.log("Inscrição feita:", response);
        setVerifyCourse((prev: Registration[]) => [
          ...prev,
          {
            id: response.data.id,
            course_id,
            student_id: userData.id,
          },
        ]);
      })
      .catch((error) => console.log(error));
  }
  return (
    <Box className="pl-5 flex gap-5">
      {data.map((course: Course) => {
        return (
          <Card className="w-70" key={course.id}>
            <CardContent className="">
              <Typography fontWeight={600}>{course?.name}</Typography>
              <CardMedia component="iframe" src={course?.video} />
            </CardContent>
            {getUserData().role === "student" ? (
              <CardActions className="flex justify-center">
                {verifyCourse?.some((c: Course) => c.id === course.id) ? (
                  <Button size="small" variant="contained" color="success" endIcon={<DoneAllOutlined/>}>
                    Inscrito
                  </Button>
                ) : (
                  <Button
                    size="small"
                    variant="contained"
                    onClick={() => submit(Number(course.id))}
                  >
                    Inscrever-se
                  </Button>
                )}
              </CardActions>
            ) : (
              ""
            )}
          </Card>
        );
      })}
    </Box>
  );
}
