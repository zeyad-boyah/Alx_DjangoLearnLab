Custom Permissions Setup:

Model: Book
Custom Permissions:
  - can_view: Allows viewing of Book instances.
  - can_create: Allows creation of Book instances.
  - can_edit: Allows editing of Book instances.
  - can_delete: Allows deletion of Book instances.

Groups:
  - Editors: Assigned can_create and can_edit.
  - Viewers: Assigned can_view.
  - Admins: Assigned all permissions.

Usage in Views:
  Use the @permission_required decorator to enforce permissions. For example:
    @permission_required('bookshelf.can_edit', raise_exception=True)
    def edit_Book(request, pk):
        ...
