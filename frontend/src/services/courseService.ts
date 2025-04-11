import axios from "axios";

const axiosInstance = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export class CourseService {
  list(){
    return axiosInstance.get('/course')
  }
  get_course_by_id(id: string) {
    return axiosInstance.get(`/course/${id}`);
  }
  create(body: { name: string; video: string, teacher_id: number }) {
    return axiosInstance.post(`/course`, body);
  }
}
