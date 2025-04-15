import axios from "axios";

const axiosInstance = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export class CourseService {
  list(){
    return axiosInstance.get('/course')
  }
  course_by_id(id: string) {
    return axiosInstance.get(`/course/${id}`);
  }
  course_by_teacher_id(id: string) {
    return axiosInstance.get(`/course/teacher/${id}`);
  }
  create(body: { name: string; video: string, teacher_id: number }) {
    return axiosInstance.post(`/course`, body);
  }
}