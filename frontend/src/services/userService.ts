import axios from "axios";

const axiosInstance = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export class UserService {
  list() {
    return axiosInstance.get("/users");
  }
  login(body: { email: string; password: string }) {
    return axiosInstance.post(`/login`, body);
  }
}
