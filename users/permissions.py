# from fastapi import HTTPException, status


# class PermissionChecker:
#     def __init__(self, required_permissions: list[int]) -> None:
#         self.required_permissions = required_permissions

#     def check_permission(self, permissions: list[int]):
#         if permissions == None:
#             raise HTTPException(
#                     status_code=status.HTTP_401_UNAUTHORIZED,
#                     detail=f'Wrong Permissions, required: {self.required_permissions}')
#         for r_perm in permissions:
#             if r_perm in self.required_permissions:
#                 return True
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail=f'Wrong Permissions, required: {self.required_permissions}')
            
    