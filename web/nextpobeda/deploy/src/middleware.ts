import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

const SECRET_ADMIN_VALUE = "vEry_c0mpl3x_s3cr3t_v4lue_th4t_n0b0dy_c4n_gu3ss_12345678901234567890";

export function middleware(request: NextRequest) {
  if (request.nextUrl.pathname === '/flag') {
    const adminCookie = request.cookies.get('admin')?.value;

    if (adminCookie !== SECRET_ADMIN_VALUE) {
      return NextResponse.redirect(new URL('/', request.url));
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/flag'],
}