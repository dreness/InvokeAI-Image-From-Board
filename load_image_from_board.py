from invokeai.app.invocations.primitives import (
    ImageField,
    ImageOutput,
    BoardField
)

from invokeai.app.invocations.baseinvocation import (
    BaseInvocation,
    InputField,
    InvocationContext,
    invocation,
)

@invocation(
    "LoadImageFromBoard",
    title="Load Newest Image From Board",
    tags=["image", "load", "board"],
    category="image",
    version="0.0.1",
)
class LoadImageFromBoard(BaseInvocation):
    """Load the newest image from the selected board and provide it as output."""

    # Inputs
    input_board: BoardField = InputField(
        description="Input board from which to fetch an image"
    )

    def invoke(self, context: InvocationContext) -> ImageOutput:
        from invokeai.app.api.dependencies import ApiDependencies

        board_id = self.input_board.board_id
        if not board_id:
            raise ValueError("Couldn't find the board?!")

        all_image_names_in_board = (
            context.services.board_images.get_all_board_image_names_for_board(board_id)
        )

        if len(all_image_names_in_board) == 0:
            raise ValueError("No images found for the specified board.")

        # images are ordered by date by default; newest at the end
        latest_img_name = all_image_names_in_board[-1]
        latest_img = ApiDependencies.invoker.services.images.get_dto(latest_img_name)

        return ImageOutput(
            image=ImageField(image_name=latest_img.image_name),
            width=latest_img.width,
            height=latest_img.height,
        )
