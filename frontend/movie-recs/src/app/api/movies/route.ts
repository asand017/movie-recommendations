import { NextRequest, NextResponse } from "next/server";

export async function GET(req: NextRequest) {
    try {
      // Here you can add logic to fetch movies from a database or an external API
      return NextResponse.json({"data": "wanna fook?"});
    } catch (error) {
      return NextResponse.error();
    }
  }
  
//   export async function POST(req: NextRequest) {
//     try {
//       const newMovie = await req.json();
//       // Here you can add logic to save the new movie to a database
//       movies.push(newMovie); // This is just an example, you should handle data persistence properly
//       return NextResponse.json(newMovie);
//     } catch (error) {
//       return NextResponse.error();
//     }
//   }