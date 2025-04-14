enum UserRoles {
    STUDENT = 'student',
    TEACHER = 'teacher',
    ADMIN = 'admin'
}

export type User = {
    email: string;
    id: number;
    name: string;
    role: UserRoles;
  };
  
export type UserProps = {
    user: User;
};