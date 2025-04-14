import axios from "axios";

const axiosInstance = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export class RegistrationService {
  create(body: { student_id: number, course_id: number }) {
    return axiosInstance.post(`/registration`, body);
  }
  list_by_student_id(id: number){
    return axiosInstance.get(`/registration/student/${id}`)
  }
}
