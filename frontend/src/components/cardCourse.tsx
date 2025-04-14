import { useEffect, useState } from "react";
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
import { UserProps } from "@/types/user";
import { Course } from "@/types/course";
import { Registration } from "@/types/registration";


export function CardCourse({ user }: UserProps) {
  const courseService = new CourseService();
  const registrationService = new RegistrationService();

  const [courses, setCourses] = useState<Course[]>([]);
  const [registrations, setRegistrations] = useState<Registration[]>([]);
  const [data, setData] = useState<Course[]>([]);

  const getUserData = () => {
    const data = localStorage.getItem("dataUser");
    return data ? JSON.parse(data) : null;
  };
  
  useEffect(() => {
    if (user.role === "teacher") {
      courseService
        .course_by_teacher_id(user.id.toString())
        .then((response) => {
          setData(response.data);
        })
        .catch((error) => console.error(error));
    }
  }, [user.id, user.role]);

  useEffect(() => {
    const userData = getUserData();
    if (userData.role === "student") {
      if (!userData) return;

      registrationService
        .list_by_student_id(userData.id)
        .then(async (response) => {
          setRegistrations(response.data);

          const coursePromises = response.data.map((reg: Registration) =>
            courseService.course_by_id(reg.course_id.toString())
          );
          const courseResponses = await Promise.all(coursePromises);
          const allCourses = courseResponses.flatMap((res) => res.data);

          setCourses(allCourses);
        })
        .catch((error) => console.error(error));
    }
  }, [user.role]);

  const submit = (course_id: number) => {
    const userData = getUserData();
    if (!userData) return;

    registrationService
      .create({ student_id: userData.id, course_id })
      .then((response) => {
        setRegistrations((prev) => [
          ...prev,
          {
            id: response.data.id,
            course_id,
            student_id: userData.id,
          },
        ]);
      })
      .catch((error) => console.error(error));
  };
  return (
    <Box className="pl-5 flex gap-5 flex-wrap">
      {user.role === "student"
        ? courses.map((course) => {
            return (
              <Card className="w-70" key={course.id}>
                <CardContent>
                  <Typography fontWeight={600}>{course.name}</Typography>
                  <CardMedia component="iframe" src={course.video} />
                </CardContent>
              </Card>
            );
          })
        : data.map((course) => {
            const isRegistered = registrations.some(
              (reg) => reg.course_id.toString() === course.id.toString()
            );
            return (
              <Card className="w-70" key={course.id}>
                <CardContent>
                  <Typography fontWeight={600}>{course.name}</Typography>
                  <CardMedia component="iframe" src={course.video} />
                </CardContent>
                <CardActions className="flex justify-center">
                  {isRegistered ? (
                    <Button
                      size="small"
                      variant="contained"
                      color="success"
                      endIcon={<DoneAllOutlined />}
                    >
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
              </Card>
            );
          })}
    </Box>
  );
}
