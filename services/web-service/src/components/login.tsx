"use client";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useState } from "react";
import { useAuth } from "@/features/auth/hooks";
 


export default function LoginForm() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const { login } = useAuth();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        console.log("Submit wurde ausgelöst!");

        try{
            await login(username, password)
        } catch (error) {
            console.error("Fehler:");
        }
    }


  return (
    <div className="flex items-center justify-center min-h-screen">
    <Card className="w-full max-w-lg">
    <form onSubmit={handleSubmit}>
        <CardHeader>
            <CardTitle className="w-full text-3xl">Login</CardTitle>
            <CardDescription className="text-center">
                Enter your AD username and password below to login
            </CardDescription>
        </CardHeader>

        <CardContent>
            <div className="flex flex-col gap-4 mt-3">
                <div className="grid gap-2 text-3xl">
                <Label htmlFor="username">Username</Label>
                <Input
                    id="username"
                    type="text"
                    placeholder="Adsync.Trainee"
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
                </div>
                <div className="grid gap-2">
                <div className="flex items-center">
                    <Label htmlFor="password">Password</Label>
                </div>
                <Input 
                    id="password"
                    type="password"
                    onChange={(e) => setPassword(e.target.value)}
                    required />
                </div>
            </div>
        </CardContent>

        <CardFooter className="flex-col gap-2 mt-6">
            <Button type="submit" className="w-full">
                Login
            </Button>
        </CardFooter>
    </form>
    </Card>
    </div>
  )
}
