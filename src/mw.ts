import * as jwt from 'jsonwebtoken';
import createError from 'http-errors';

export function getJWT(user): {access_token: string} {
  const payload = {
    id: user.id,
  };

  return {
    access_token: jwt.sign(payload, process.env.JWT_SECRET!),
  };
}

export const getMe = async (ctx, next) => {
  const rawjwt = ctx.headers.authorization?.split(' ')?.[1];

  if (rawjwt) {
    const payload = jwt.verify(rawjwt, process.env.JWT_SECRET!) as {
      id: string;
    };
    ctx.state.user = payload;
  }
  await next();
};

export const roleGuard =
  (allowed: ('inactive' | 'user' | 'admin')[]) => async (ctx, next) => {
    if (!allowed.includes(ctx.state.user.role)) {
      throw createError(401);
    }

    await next();
  };
